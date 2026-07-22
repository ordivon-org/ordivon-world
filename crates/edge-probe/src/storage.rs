use std::fs::{self, File, OpenOptions};
use std::io::{BufRead, BufReader, BufWriter, Write};
use std::path::Path;

use anyhow::{Context, Result, bail};
use edge_model::ProbeResult;

pub fn append_results(path: &Path, results: &[ProbeResult]) -> Result<()> {
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)
            .with_context(|| format!("failed to create {}", parent.display()))?;
    }
    let file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(path)
        .with_context(|| format!("failed to open {}", path.display()))?;
    let mut writer = BufWriter::new(file);
    for result in results {
        serde_json::to_writer(&mut writer, result)?;
        writer.write_all(b"\n")?;
    }
    writer.flush()?;
    Ok(())
}

pub fn read_results(path: &Path) -> Result<Vec<ProbeResult>> {
    let file = File::open(path).with_context(|| format!("failed to open {}", path.display()))?;
    let reader = BufReader::new(file);
    let mut results = Vec::new();
    for (index, line) in reader.lines().enumerate() {
        let line = line.with_context(|| format!("failed reading line {}", index + 1))?;
        if line.trim().is_empty() {
            continue;
        }
        let result = serde_json::from_str(&line)
            .with_context(|| format!("invalid NDJSON at line {}", index + 1))?;
        results.push(result);
    }
    if results.is_empty() {
        bail!("no probe results found in {}", path.display());
    }
    Ok(results)
}

pub fn write_text(path: &Path, content: &str) -> Result<()> {
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)
            .with_context(|| format!("failed to create {}", parent.display()))?;
    }
    fs::write(path, content).with_context(|| format!("failed to write {}", path.display()))
}
