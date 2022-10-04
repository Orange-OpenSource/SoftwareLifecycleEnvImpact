export async function getCpuModels(): Promise<string[]> {
	return [
		'Xeon E5-2666 v3',
		'Xeon E5-2676 v3',
		'Xeon E5-2686 v4',
		'Xeon E5-2650',
		'Xeon E5-2665',
		'Xeon E5-2670',
		'Xeon E5-2651 v2',
		'Xeon E5-2670 v2',
		'Xeon E5-2680 v2',
		'Xeon E7-8880 v3',
		'Xeon Platinum 8124M',
		'Xeon Platinum 8151',
		'Xeon Platinum 8175M',
		'Xeon Platinum 8176M',
		'Xeon Platinum 8252C',
		'Xeon Platinum 8259CL',
		'Xeon Platinum 8275CL',
		'Xeon Platinum 8375C',
		'EPYC 7571',
		'EPYC 7R32',
		'Graviton',
		'Graviton2',
		'Core i7-8700B'
	];
}

export async function getCpuFamilies(): Promise<string[]> {
	return ['Skylake', 'Coffee Lake', 'Broadwell', 'Haswell', 'Ivy Bridge', 'Sandy Bridge', 'Ice Lake', 'Kaby Lake', 'Zen2', 'Zen3', 'Graviton2'];
}
export async function getCpuInfos() {
	/*TODO interace */
	return {
		models: await getCpuModels(),
		families: await getCpuFamilies()
	};
}
