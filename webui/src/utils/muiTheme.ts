import { createTheme } from "@mui/material/styles";

// GitHub Dark Mode theme
export const githubDarkTheme = createTheme({
  palette: {
    mode: "dark",
    primary: {
      main: "#58a6ff", // GitHub dark blue
      light: "#79c0ff",
      dark: "#388bfd",
    },
    secondary: {
      main: "#7d8590", // GitHub dark gray
    },
    background: {
      default: "#0d1117", // GitHub dark background
      paper: "#161b22", // GitHub dark card background
    },
    text: {
      primary: "#f0f6fc", // GitHub dark primary text
      secondary: "#7d8590", // GitHub dark secondary text
    },
    divider: "#30363d", // GitHub dark border
    success: {
      main: "#238636", // GitHub dark green
    },
  },
  typography: {
    fontFamily:
      '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif',
    h1: {
      fontWeight: 600,
      fontSize: "3rem",
      lineHeight: 1.125,
      color: "#f0f6fc",
    },
    h2: {
      fontWeight: 600,
      fontSize: "2rem",
      lineHeight: 1.25,
      color: "#f0f6fc",
    },
    h3: {
      fontWeight: 600,
      fontSize: "1.5rem",
      lineHeight: 1.25,
      color: "#f0f6fc",
    },
    body1: {
      fontSize: "1rem",
      lineHeight: 1.5,
      color: "#7d8590",
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: "none",
          fontWeight: 500,
          borderRadius: "6px",
          padding: "8px 16px",
        },
        contained: {
          backgroundColor: "#238636", // GitHub dark green
          color: "#ffffff",
          boxShadow: "0 1px 0 rgba(27,31,36,0.04)",
          "&:hover": {
            backgroundColor: "#2ea043",
            boxShadow: "0 1px 0 rgba(27,31,36,0.1)",
          },
        },
        outlined: {
          borderColor: "#30363d",
          color: "#f0f6fc",
          backgroundColor: "#21262d",
          "&:hover": {
            backgroundColor: "#30363d",
            borderColor: "#30363d",
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          border: "1px solid #30363d",
          borderRadius: "6px",
          boxShadow: "none",
          backgroundColor: "#0d1117",
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          "& .MuiOutlinedInput-root": {
            borderRadius: "6px",
            backgroundColor: "#0d1117",
            color: "#f0f6fc",
            "& fieldset": {
              borderColor: "#30363d",
            },
            "&:hover fieldset": {
              borderColor: "#58a6ff",
            },
            "&.Mui-focused fieldset": {
              borderColor: "#58a6ff",
              borderWidth: "1px",
            },
          },
          "& .MuiOutlinedInput-input": {
            color: "#f0f6fc",
            "&::placeholder": {
              color: "#7d8590",
              opacity: 1,
            },
          },
        },
      },
    },
    MuiAccordion: {
      styleOverrides: {
        root: {
          border: "1px solid #30363d",
          borderRadius: "6px",
          boxShadow: "none",
          backgroundColor: "#161b22",
          "&:before": {
            display: "none",
          },
          "&:not(:last-child)": {
            marginBottom: "8px",
          },
        },
      },
    },
    MuiAccordionSummary: {
      styleOverrides: {
        root: {
          "&:hover": {
            backgroundColor: "#21262d",
          },
        },
      },
    },
    MuiDialog: {
      styleOverrides: {
        paper: {
          background: "#010409",
          border: "1px solid #30363d",
          borderRadius: "12px",
          "& .MuiPaper-root": {
            background: "#010409",
          },
          "& .MuiBackdrop-root": {
            backgroundColor: "transparent", // Try to remove this to see the result
          },
        },
      },
    },
  },
});