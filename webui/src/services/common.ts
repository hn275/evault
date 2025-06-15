// Whenever the session expires, this wrapper would redirect the user to the home page.
// This should be used for all API calls that require authentication.
export const fetchWithRedirect = async (url: string, options?: RequestInit) => {
  return fetch(url, options)
    .then((r) => {
      if (r.status === 440) {
        window.location.href = "/";
      }
      return r;
    })
    .catch((e) => {
      throw e;
    });
};
