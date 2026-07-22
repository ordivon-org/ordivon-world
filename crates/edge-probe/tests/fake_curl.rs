#[cfg(unix)]
mod unix {
    use std::fs;
    use std::os::unix::fs::PermissionsExt;
    use std::time::Duration;

    use edge_model::{ProbeProtocol, TargetConfig};
    use edge_probe::{ProbeOptions, run_probe};
    use tempfile::tempdir;

    #[test]
    fn command_runner_parses_curl_json() {
        let directory = tempdir().expect("temp directory");
        let script = directory.path().join("fake-curl");
        fs::write(
            &script,
            r#"#!/bin/sh
printf '%s' '{"response_code":200,"remote_ip":"203.0.113.10","time_namelookup":0.001,"time_connect":0.004,"time_appconnect":0.010,"time_starttransfer":0.020,"time_total":0.025}'
"#,
        )
        .expect("write fake curl");
        let mut permissions = fs::metadata(&script).expect("metadata").permissions();
        permissions.set_mode(0o755);
        fs::set_permissions(&script, permissions).expect("permissions");

        let target = TargetConfig {
            id: "example".into(),
            url: "https://example.com/".into(),
            enabled: true,
            protocols: vec![ProbeProtocol::HttpTls],
        };
        let options = ProbeOptions {
            network: "test-network".into(),
            route: "test-route".into(),
            timeout: Duration::from_secs(2),
            no_env_proxy: true,
            curl_bin: script.display().to_string(),
        };

        let result = run_probe(&target, ProbeProtocol::HttpTls, &options);
        assert!(result.success);
        assert_eq!(result.http_status, Some(200));
        assert_eq!(result.remote_ip.as_deref(), Some("203.0.113.10"));
        assert_eq!(result.dns_ms, Some(1.0));
        assert_eq!(result.connect_ms, Some(3.0));
        assert_eq!(result.tls_ms, Some(6.0));
        assert_eq!(result.total_ms, Some(25.0));
    }
}
