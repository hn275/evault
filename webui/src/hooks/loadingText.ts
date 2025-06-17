import { useEffect, useState } from "react";

/**
 * Changing loading text at `changeInterval` ms.
 * Returns the index of the active loading text to be rendrered.
 * */
export function useLoadingText(changeInterval: number, loadingTexts: string[]) {
  const lineCtr = loadingTexts.length;
  const [index, setIndex] = useState(Math.floor(Math.random() * lineCtr));

  useEffect(() => {
    const intervalID = setInterval(() => {
      const nextIndex = Math.floor(Math.random() * lineCtr);
      setIndex(nextIndex);
    }, changeInterval);
    return () => clearInterval(intervalID);
  }, [lineCtr, changeInterval]);

  return { index };
}
