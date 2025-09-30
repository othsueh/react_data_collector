<script lang="ts">
	let { data } = $props();

	let inSession = $state<boolean>(!!data.inStudentSession);
	let count = $state(0);
	let result = $state<number[]>([]);

	$effect(() => {
		inSession = !!data.inStudentSession;
	});

	function push(val: number) {
		if (!inSession) return;
		if (count >= data.n_cycles) return;
		result = [...result, val];
		count = result.length;
		// Auto-submit when full
		if (count >= data.n_cycles) {
			queueMicrotask(() => {
				const form = document.getElementById('mrecord-form') as HTMLFormElement | null;
				form?.requestSubmit();
			});
		}
	}
</script>

<div class="min-h-screen bg-white flex flex-col items-center mt-24 md:mt-24 px-4">
	<h2 class="text-theme font-bold italic text-t2 text-center">mrecord</h2>
	<div class="flex flex-col items-center mb-12">
		<svg width="192" height="8" class="mb-1"><rect x="0" y="0" width="192" height="6" class="fill-theme"/></svg>
		<svg width="192" height="8"><rect x="0" y="0" width="192" height="6" class="fill-theme"/></svg>
	</div>

	{#if !inSession}
		<div class="text-label font-bold italic text-t3 text-center space-y-8 mt-8">
			<div>
				<p>Not</p>
				<p>In A</p>
				<p>Session</p>
			</div>
		</div>
	{:else}
		<div class="w-full flex flex-col items-center max-w-md space-y-2 text-label text-hl font-bold mb-6">
			<p>擊球者： {data.studentName}</p>
			<p>擊球數： {count} / {data.n_cycles}</p>
		</div>

		<form id="mrecord-form" class="w-full max-w-xs space-y-5" method="POST" action="?/submit">
			<input type="hidden" name="sessionId" value={data.sessionId} />
			<input type="hidden" name="studentId" value={data.studentId} />
			<input type="hidden" name="studentSessionId" value={data.studentSessionId} />
			<input type="hidden" name="hit_miss_array" value={JSON.stringify(result)} />

			<div class="w-full max-w-xs space-y-4">
				<button class="w-full rounded-3xl py-16 font-bold text-white text-t2 bg-blue-500" type="button" onclick={() => push(1)}>打 / 不接</button>
				<button class="w-full rounded-3xl py-16 font-bold text-white text-t2 bg-pink-500" type="button" onclick={() => push(0)}>接 / 不打</button>
			</div>

			<!-- Invisible submit target for server action -->
		</form>
	{/if}
</div>
