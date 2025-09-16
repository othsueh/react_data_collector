<script lang="ts">
	import { Button } from '$lib';
	import { backendFetch } from '$lib/api';
	let { data } = $props();

	let inSession = $state<boolean>(!!data.inStudentSession);
	let count = $state(0);
	let result = $state<number[]>([]);
	let n_cycles = $state<number>(data.n_cycles ?? 0);
	let waitingFor = $state<string | null>(data.waitFor ?? null);

	$effect(() => {
		inSession = !!data.inStudentSession;
		waitingFor = data.waitFor ?? null;
	});

	async function pollUntilChanged() {
		const interval = 1500;
		const tick = async () => {
			try {
				const res = await backendFetch(fetch, '/student-sessions/current');
				const cur = await res.json();
				const curId = cur?.student_session_uuid ?? null;
				if (!curId || curId !== waitingFor) {
					location.replace('/mrecord');
					return;
				}
			} catch {}
			setTimeout(tick, interval);
		};
		setTimeout(tick, interval);
	}

	function push(val: number) {
		if (!inSession || waitingFor) return;
		if (count >= n_cycles) return;
		result = [...result, val];
		count = result.length;
		if (count >= n_cycles) {
			queueMicrotask(() => {
				const form = document.getElementById('mrecord-form') as HTMLFormElement | null;
				form?.requestSubmit();
			});
		}
	}

	$effect(() => {
		if (waitingFor) pollUntilChanged();
	});
</script>

<div class="mt-24 flex min-h-screen flex-col items-center bg-white px-4 md:mt-24">
	<h2 class="text-theme text-t2 text-center font-bold italic">mrecord</h2>
	<div class="mb-12 flex flex-col items-center">
		<svg width="192" height="8" class="mb-1"
			><rect x="0" y="0" width="192" height="6" class="fill-theme" /></svg
		>
		<svg width="192" height="8"><rect x="0" y="0" width="192" height="6" class="fill-theme" /></svg>
	</div>

	{#if waitingFor}
		<div class="text-label text-t3 mt-8 space-y-4 text-center font-bold italic">
			<p>Please wait for the current student session to complete.</p>
			<p class="text-xs">(This page will refresh automatically.)</p>
		</div>
	{:else if !inSession}
		<div class="text-label text-t3 mt-8 space-y-8 text-center font-bold italic">
			<div>
				<p>Not</p>
				<p>In A</p>
				<p>Session</p>
			</div>
		</div>
	{:else}
		<div
			class="text-label text-hl mb-6 flex w-full max-w-md flex-col items-center space-y-2 font-bold"
		>
			<p>擊球者： {data.studentName}</p>
			<p>擊球數： {count} / {data.n_cycles}</p>
		</div>

		<form id="mrecord-form" class="w-full max-w-xs space-y-5" method="POST" action="?/submit">
			<input type="hidden" name="sessionId" value={data.sessionId} />
			<input type="hidden" name="studentId" value={data.studentId} />
			<input type="hidden" name="studentSessionId" value={data.studentSessionId} />
			<input type="hidden" name="hit_miss_array" value={JSON.stringify(result)} />

			<div class="w-full max-w-xs space-y-4">
				<button
					class="text-t2 w-full rounded-3xl bg-blue-500 py-16 font-bold text-white"
					type="button"
					onclick={() => push(1)}>打 / 不接</button
				>
				<button
					class="text-t2 w-full rounded-3xl bg-pink-500 py-16 font-bold text-white"
					type="button"
					onclick={() => push(0)}>接 / 不打</button
				>
			</div>
		</form>
	{/if}
</div>
