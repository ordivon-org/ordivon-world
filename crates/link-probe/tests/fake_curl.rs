#[cfg(unix)]
mod unix {
    use std::fs::{self, File};
    use std::io::Write;
    use std::os::unix::fs::PermissionsExt;
    use std::path::Path;
    use std::process::Stdio;
    use std::thread;
    use std::time::{Duration, Instant};

    use link_model::{FailureClass, ProbeKind, ProbeProtocol, ProbeTermination, TargetConfig};
    use link_probe::{ProbeOptions, run_probe};
    use tempfile::tempdir;

    fn write_script(path: &Path, body: &str) {
        let mut file = File::create(path).expect("create fake curl");
        file.write_all(format!("#!/bin/sh\n{body}\n").as_bytes())
            .expect("write fake curl");
        file.sync_all().expect("sync fake curl");
        drop(file);

        let mut permissions = fs::metadata(path).expect("metadata").permissions();
        permissions.set_mode(0o755);
        fs::set_permissions(path, permissions).expect("permissions");
        // WSL/overlay filesystems can briefly return ETXTBSY when a newly
        // written file is executed immediately by parallel tests.
        thread::sleep(Duration::from_millis(10));
    }

    fn target() -> TargetConfig {
        TargetConfig {
            id: "example".into(),
            url: "https://example.com/".into(),
            enabled: true,
            protocols: vec![ProbeProtocol::HttpTls],
        }
    }

    fn options(script: &Path, probe_kind: ProbeKind) -> ProbeOptions {
        ProbeOptions {
            network: "test-network".into(),
            route: "test-route".into(),
            timeout: Duration::from_secs(5),
            no_env_proxy: true,
            curl_bin: script.display().to_string(),
            probe_kind,
            collection_id: "test-collection".into(),
            sample_index: 1,
            requested_duration: None,
            rate_limit_bytes_per_second: None,
        }
    }

    #[test]
    fn reachability_uses_head_and_parses_curl_json() {
        let directory = tempdir().expect("temp directory");
        let script = directory.path().join("fake-curl");
        write_script(
            &script,
            r#"case " $* " in
  *" --head "*) ;;
  *) exit 97 ;;
esac
printf '%s' '{"response_code":200,"remote_ip":"203.0.113.10","time_namelookup":0.001,"time_connect":0.004,"time_appconnect":0.010,"time_starttransfer":0.020,"time_total":0.025,"size_download":0,"speed_download":0,"num_connects":1,"http_version":"1.1"}'"#,
        );

        let result = run_probe(
            &target(),
            ProbeProtocol::HttpTls,
            &options(&script, ProbeKind::Reachability),
        );
        assert!(result.success, "{result:#?}");
        assert_eq!(result.http_status, Some(200));
        assert_eq!(result.remote_ip.as_deref(), Some("203.0.113.10"));
        assert_eq!(result.dns_ms, Some(1.0));
        assert_eq!(result.connect_ms, Some(3.0));
        assert_eq!(result.tls_ms, Some(6.0));
        assert_eq!(result.total_ms, Some(25.0));
        assert_eq!(result.bytes_downloaded, Some(0));
        assert_eq!(result.connection_count, Some(1));
    }

    #[test]
    fn transfer_requires_body_mode_and_records_bytes() {
        let directory = tempdir().expect("temp directory");
        let script = directory.path().join("fake-curl");
        write_script(
            &script,
            r#"case " $* " in
  *" --head "*) exit 97 ;;
esac
printf '%s' '{"response_code":200,"time_namelookup":0.001,"time_connect":0.004,"time_appconnect":0.010,"time_starttransfer":0.020,"time_total":2.5,"size_download":1048576,"speed_download":419430,"num_connects":1,"http_version":"1.1"}'"#,
        );

        let result = run_probe(
            &target(),
            ProbeProtocol::HttpTls,
            &options(&script, ProbeKind::Transfer),
        );
        assert!(result.success, "{result:#?}");
        assert_eq!(result.bytes_downloaded, Some(1_048_576));
        assert_eq!(result.speed_download_bps, Some(419_430.0));
        assert_eq!(result.termination, Some(ProbeTermination::Completed));
    }

    #[test]
    fn hung_probe_process_is_killed_by_the_hard_timeout() {
        let directory = tempdir().expect("temp directory");
        let script = directory.path().join("fake-curl");
        let pid_path = directory.path().join("fake-curl.pid");
        write_script(
            &script,
            &format!("echo $$ > '{}'; exec sleep 60", pid_path.display()),
        );

        let mut options = options(&script, ProbeKind::Reachability);
        options.timeout = Duration::from_secs(1);
        let started = Instant::now();
        let result = run_probe(&target(), ProbeProtocol::HttpTls, &options);
        assert!(started.elapsed() < Duration::from_secs(4));
        assert!(!result.success);
        assert_eq!(result.failure_class, Some(FailureClass::Timeout));
        assert_eq!(
            result.error.as_deref(),
            Some("probe process exceeded its hard timeout")
        );

        thread::sleep(Duration::from_millis(100));
        let pid = fs::read_to_string(&pid_path).expect("pid");
        let status = std::process::Command::new("kill")
            .args(["-0", pid.trim()])
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .status()
            .expect("process check");
        assert!(!status.success(), "timed-out probe process still exists");
    }

    #[test]
    fn lifetime_treats_expected_deadline_as_success() {
        let directory = tempdir().expect("temp directory");
        let script = directory.path().join("fake-curl");
        write_script(
            &script,
            r#"case " $* " in
  *" --head "*) exit 97 ;;
esac
printf '%s' '{"response_code":200,"time_namelookup":0.001,"time_connect":0.004,"time_appconnect":0.010,"time_starttransfer":0.020,"time_total":5.001,"size_download":329315,"speed_download":65852,"num_connects":1,"http_version":"1.1"}'
printf '%s\n' 'curl: (28) expected deadline' >&2
exit 28"#,
        );

        let mut options = options(&script, ProbeKind::ConnectionLifetime);
        options.requested_duration = Some(Duration::from_secs(5));
        options.rate_limit_bytes_per_second = Some(65_536);
        let result = run_probe(&target(), ProbeProtocol::HttpTls, &options);

        assert!(result.success, "{result:#?}");
        assert_eq!(result.tool_exit_code, Some(28));
        assert_eq!(result.termination, Some(ProbeTermination::DeadlineReached));
        assert_eq!(result.failure_class, None);
        assert_eq!(result.error, None);
    }
}
