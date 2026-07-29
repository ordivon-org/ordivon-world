#[cfg(unix)]
mod unix {
    use std::fs;
    use std::os::unix::fs::PermissionsExt;
    use std::process::Command;

    use link_model::{ProbeKind, ProbeResult};
    use tempfile::tempdir;

    #[test]
    fn repeated_collection_preserves_identity_and_sample_index() {
        let directory = tempdir().expect("temp directory");
        let registry = directory.path().join("targets.toml");
        let curl = directory.path().join("fake-curl");
        let output = directory.path().join("results.ndjson");

        fs::write(
            &registry,
            r#"schema_version = 1

[[targets]]
id = "example"
url = "https://example.com/"
enabled = true
protocols = ["http_tls"]
"#,
        )
        .expect("write registry");
        fs::write(
            &curl,
            r#"#!/bin/sh
case " $* " in
  *" --head "*) ;;
  *) exit 97 ;;
esac
printf '%s' '{"response_code":200,"time_namelookup":0.001,"time_connect":0.004,"time_appconnect":0.010,"time_starttransfer":0.020,"time_total":0.025,"size_download":0,"speed_download":0,"num_connects":1,"http_version":"1.1"}'
"#,
        )
        .expect("write fake curl");
        let mut permissions = fs::metadata(&curl).expect("metadata").permissions();
        permissions.set_mode(0o755);
        fs::set_permissions(&curl, permissions).expect("permissions");

        let execution = Command::new(env!("CARGO_BIN_EXE_link-probe"))
            .args([
                "run",
                "--targets",
                registry.to_str().expect("registry path"),
                "--network",
                "test-network",
                "--route",
                "direct-process",
                "--protocol",
                "http-tls",
                "--repeat",
                "2",
                "--interval-seconds",
                "0",
                "--no-env-proxy",
                "--truncate-output",
                "--curl-bin",
                curl.to_str().expect("curl path"),
                "--output",
                output.to_str().expect("output path"),
            ])
            .output()
            .expect("run link-probe");
        assert!(
            execution.status.success(),
            "stdout: {}\nstderr: {}",
            String::from_utf8_lossy(&execution.stdout),
            String::from_utf8_lossy(&execution.stderr),
        );

        let raw = fs::read_to_string(output).expect("read output");
        let results: Vec<ProbeResult> = raw
            .lines()
            .map(|line| serde_json::from_str(line).expect("probe result"))
            .collect();

        assert_eq!(results.len(), 2);
        assert_eq!(results[0].probe_kind, ProbeKind::Reachability);
        assert_eq!(results[0].sample_index, Some(1));
        assert_eq!(results[1].sample_index, Some(2));
        assert_eq!(results[0].collection_id, results[1].collection_id);
        assert!(results.iter().all(|result| result.success));
    }
}
