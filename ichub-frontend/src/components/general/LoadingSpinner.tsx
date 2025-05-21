import { Box } from '@mui/material'

const LoadingSpinner = () => {
  return (
    <Box
      sx={{
        width: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        margin: "auto",
        height: "100%",
      }}
    >
      <span className="spinner"></span>
    </Box>
  )
}

export default LoadingSpinner