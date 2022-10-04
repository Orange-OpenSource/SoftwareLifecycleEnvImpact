import { get } from "./api";

export async function getCountries(): Promise<string[] | [string, unknown][]> {
	const res = await get('utils/country_code');
	return res.text().then((json) => {
		return Object.entries(JSON.parse(json))
	});
}