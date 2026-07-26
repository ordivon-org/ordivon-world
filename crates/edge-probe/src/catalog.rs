use std::fmt::Write as _;
use std::fs;
use std::path::Path;

use anyhow::{Context, Result};
use edge_model::TransportCatalog;

pub fn load_transport_catalog(path: &Path) -> Result<TransportCatalog> {
    let raw = fs::read_to_string(path)
        .with_context(|| format!("failed to read transport catalog {}", path.display()))?;
    let catalog: TransportCatalog = toml::from_str(&raw)
        .with_context(|| format!("failed to parse transport catalog {}", path.display()))?;
    catalog.validate().context("invalid transport catalog")?;
    Ok(catalog)
}

pub fn transport_catalog_markdown(catalog: &TransportCatalog) -> String {
    let mut output = String::new();
    writeln!(output, "# Transport catalog").expect("write to string");
    writeln!(output).expect("write to string");
    writeln!(output, "Inspected at: `{}`", catalog.inspected_at).expect("write to string");
    writeln!(output).expect("write to string");
    writeln!(
        output,
        "| ID | Role | Layers | Carriers | Source status | License |"
    )
    .expect("write to string");
    writeln!(output, "|---|---|---|---|---|---|").expect("write to string");

    for transport in &catalog.transports {
        writeln!(
            output,
            "| `{}` | {} | {} | {} | {} | {} |",
            transport.id,
            transport.role,
            join_display(&transport.layers),
            join_display(&transport.carriers),
            transport.source_status,
            escape_table(&transport.license),
        )
        .expect("write to string");
    }

    for transport in &catalog.transports {
        writeln!(output).expect("write to string");
        writeln!(output, "## {}", transport.id).expect("write to string");
        writeln!(output).expect("write to string");
        writeln!(output, "- Family: `{}`", transport.family).expect("write to string");
        writeln!(output, "- Implementation: {}", transport.implementation)
            .expect("write to string");
        writeln!(output, "- Language: {}", transport.language).expect("write to string");
        writeln!(
            output,
            "- Source: {} at `{}`",
            transport.source_url, transport.source_revision
        )
        .expect("write to string");
        writeln!(output, "- Primary security: {}", transport.primary_security)
            .expect("write to string");
        writeln!(output, "- Camouflage: {}", transport.camouflage).expect("write to string");
        writeln!(output).expect("write to string");
        writeln!(output, "### Strengths").expect("write to string");
        for strength in &transport.strengths {
            writeln!(output, "- {strength}").expect("write to string");
        }
        writeln!(output).expect("write to string");
        writeln!(output, "### Limitations").expect("write to string");
        for limitation in &transport.limitations {
            writeln!(output, "- {limitation}").expect("write to string");
        }
        writeln!(output).expect("write to string");
        writeln!(output, "### Code entry points").expect("write to string");
        for path in &transport.code_paths {
            writeln!(output, "- `{path}`").expect("write to string");
        }
    }

    output
}

fn join_display<T: std::fmt::Display>(values: &[T]) -> String {
    values
        .iter()
        .map(ToString::to_string)
        .collect::<Vec<_>>()
        .join(", ")
}

fn escape_table(value: &str) -> String {
    value.replace('|', "\\|")
}

#[cfg(test)]
mod tests {
    use chrono::NaiveDate;
    use edge_model::{
        SourceStatus, StudyRole, TransportCarrier, TransportCatalog, TransportLayer,
        TransportProfile,
    };

    use super::*;

    #[test]
    fn markdown_contains_source_revision_and_limitations() {
        let catalog = TransportCatalog {
            schema_version: 1,
            inspected_at: NaiveDate::from_ymd_opt(2026, 7, 26).expect("valid date"),
            transports: vec![TransportProfile {
                id: "example".into(),
                family: "example".into(),
                implementation: "Example".into(),
                role: StudyRole::Candidate,
                source_url: "https://example.com/source".into(),
                source_revision: "0123456789abcdef0123456789abcdef01234567".into(),
                license: "MIT".into(),
                source_status: SourceStatus::OpenSource,
                language: "Rust".into(),
                layers: vec![TransportLayer::StreamProxy],
                carriers: vec![TransportCarrier::Tcp],
                primary_security: "AEAD".into(),
                camouflage: "None".into(),
                strengths: vec!["Small".into()],
                limitations: vec!["Visible endpoint".into()],
                code_paths: vec!["src/lib.rs".into()],
            }],
        };

        let markdown = transport_catalog_markdown(&catalog);
        assert!(markdown.contains("0123456789abcdef"));
        assert!(markdown.contains("Visible endpoint"));
        assert!(markdown.contains("src/lib.rs"));
    }
}
