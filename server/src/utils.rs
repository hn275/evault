use anyhow::anyhow;
use tracing::warn;

pub enum Stage {
    Development,
    Production,
}

impl Stage {
    pub fn read_from_env() -> anyhow::Result<Self> {
        use std::env;

        let stage = env::var("STAGE").unwrap_or_else(|err| {
            warn!(
                "Unable to read the environment variable `STAGE`\n
{}
Defaulting to development.",
                err
            );

            String::from("development")
        });

        match stage.as_str() {
            "development" => Ok(Self::Development),
            "production" => Ok(Self::Production),
            _ => Err(anyhow!("Unsupported staging value: {}", stage)),
        }
    }
}

pub mod env {
    use tracing::warn;

    pub fn env_or_panic(key: &'static str) -> String {
        match std::env::var(key) {
            Ok(v) => v,
            Err(err) => {
                panic!("Failed to environment variable {}:\n{}", key, err);
            }
        }
    }

    pub fn env_or_default(key: &'static str, default_value: &'static str) -> String {
        std::env::var(key).unwrap_or_else(|err| match err {
            std::env::VarError::NotPresent => {
                warn!(
                    "Variable {} not set, using default value {}",
                    key, default_value
                );
                default_value.to_string()
            }
            _ => {
                panic!("Invalid value for environment variable {}:\n{}", key, err);
            }
        })
    }
}
