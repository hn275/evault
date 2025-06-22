import { Box, Button, Chip, Typography } from "@mui/material";
import type { Repository } from "../../types/Repository";
import { Link } from "@tanstack/react-router";
import { Public, Lock } from "@mui/icons-material";

export function RepositoryCard({ repo }: { repo: Repository }) {
  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "flex-start",
        py: 3,
        borderBottom: "1px solid #2e353c",
      }}
    >
      <Box sx={{ flexGrow: 1 }}>
        <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}>
          <Typography
            variant="h6"
            component="a"
            href={`https://github.com/${repo.full_name}`}
            sx={{
              textDecoration: "none",
              color: "primary.main",
              fontWeight: 600,
              fontSize: "1.125rem",
              "&:hover": {
                textDecoration: "underline",
              },
            }}
          >
            {repo.full_name}
          </Typography>
          <Chip
            label={repo.private ? "Private" : "Public"}
            size="small"
            icon={
              repo.private ? (
                <Lock sx={{ fontSize: 12 }} />
              ) : (
                <Public sx={{ fontSize: 12 }} />
              )
            }
            sx={{
              bgcolor: "background.paper",
              border: "1px solid #30363d",
              fontSize: "12px",
              height: "20px",
              py: 1,
            }}
          />
        </Box>
        {repo.description && (
          <Typography variant="body2" sx={{ color: "#7d8590", mb: 2 }}>
            {repo.description}
          </Typography>
        )}
      </Box>
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 1,
          ml: 2,
          minWidth: "112px",
        }}
      >
        <Link
          to="/dashboard/repository/$repoID"
          params={{ repoID: `${repo.id}` }}
          search={{ repo: repo.full_name }}
        >
          <Button
            variant="contained"
            color="primary"
            size="small"
            sx={{ textTransform: "none" }}
          >
            View Vault
          </Button>
        </Link>
      </Box>
    </Box>
  );
}
