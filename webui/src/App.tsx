import { useNavigate } from "react-router";
import "./App.css";

function App() {
	const h = useHome();

	return (
		<>
			<button onClick={h.signInRedirect}>Sign In with GitHub</button>
		</>
	);
}

export default App;

function useHome() {
	const nav = useNavigate();

	async function signInRedirect() {
		const r = await fetch(`/api/auth?device_type=web`);
		const url = new URL(await r.text());
		nav(`${url.pathname}${url.search}`);
	}

	return { signInRedirect };
}
