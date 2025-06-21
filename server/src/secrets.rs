use anyhow::Context;
use base64::{Engine, engine::general_purpose::URL_SAFE_NO_PAD};
use rand::TryRngCore;
use rand::rngs::OsRng;

pub fn token_urlsafe(nbytes: usize) -> anyhow::Result<String> {
    // Generate random bytes
    let mut bytes = vec![0u8; nbytes];
    OsRng
        .try_fill_bytes(&mut bytes)
        .context("Failed to generate random bytes")?;

    Ok(URL_SAFE_NO_PAD.encode(&bytes))
}
