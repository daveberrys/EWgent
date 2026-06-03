let apiPromise: Promise<any> | null = null;

export function getPyAPI(): Promise<any> {
  if (!apiPromise) {
    apiPromise = new Promise((resolve) => {
      if (window.pywebview?.api) {
        resolve(window.pywebview.api);
        return;
      }
      window.addEventListener("pywebviewready", () => {
        resolve(window.pywebview?.api);
      });
    });
  }
  return apiPromise;
}
