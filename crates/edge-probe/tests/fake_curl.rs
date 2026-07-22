#[cfg(unix)]
mod unix {
    use std::fs;
    use std::os::unix::fs::PermissionsExt;
    use std::path::Path;
    use std::time::Duration;

    use edge_model::{ProbeKind, ProbeProtocol, ProbeTermination, TargetConfig};
    use edge_probe::{ProbeOptions, run_probe};
    use tempfile::tempdir;

    fn write_script(path: &Path, body: &str) {
        fs::write(path, format!("#!/bin/sh\n{body}\n")).expect("write fake curl");
        let mut permissions = fs::metadata(path).expect("metadata").permissions();
        permissions.set_mode(0o755);
        fs::set_permissions(path, permissions).expect("permissions");
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
