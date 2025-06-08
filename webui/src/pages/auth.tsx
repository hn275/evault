import { useEffect } from "react";
import { useSearchParams, redirect } from "react-router-dom";
// path /auth
export function Auth() {
	useAuth();

	return <>aslkdjflkd </>;
}

function useAuth() {
	const [param] = useSearchParams();
	useEffect(() => {
		const sessionId = param.get("session_id");
		(async () => {
			const r = await fetch(
				`http://localhost:8000/api/auth/token?session_id=${sessionId}`,
			);
			window.location.href = await r.text();
		})();
	}, []);
}
