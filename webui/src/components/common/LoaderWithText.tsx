import { Box, CircularProgress, Typography } from "@mui/material";

// This is a component that displays a loader with a text
export function LoaderWithText({ text }: { text: string }) {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        height: "100%",
      }}
    >
      <CircularProgress />
      <Typography>{text}</Typography>
    </Box>
  );
}
