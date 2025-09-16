<script lang="ts">
	import { Button } from '$lib';
	let { data } = $props();

	let inSession = $state<boolean>(!!data.inSession);
	let selectedStudentId = $state<number | null>(data.students?.[0]?.id ?? null);

	$effect(() => {
		inSession = !!data.inSession;
		selectedStudentId = data.students?.[0]?.id ?? null;
	});
</script>

<div class="min-h-screen bg-white flex flex-col items-center mt-24 md:mt-24 px-4">
	<h2 class="text-theme font-bold italic text-t2 text-center">record</h2>
	<div class="flex flex-col items-center mb-12">
		<svg width="192" height="8" class="mb-1"><rect x="0" y="0" width="192" height="6" class="fill-theme"/></svg>
		<svg width="192" height="8"><rect x="0" y="0" width="192" height="6" class="fill-theme"/></svg>
	</div>

	{#if !inSession}
		<div class="text-label text-t3 mt-8 space-y-8 text-center font-bold italic">
			<div>
				<p>Not</p>
				<p>In A</p>
				<p>Session</p>
				<div class="mt-2"></div>
				<p>Go to</p>
				<a href="/setting">Setting</a>
			</div>
		</div>
	{:else}
		<form class="w-full max-w-xs space-y-10" method="POST">
			<div class="flex items-center justify-between gap-6">
				<label for="student" class="text-label text-hl font-bold">擊球者</label>
				<select
					id="student"
					name="studentId"
					bind:value={selectedStudentId}
					class="min-w-20 border border-gray-400 rounded-xl px-2 py-1 text-hl text-center"
				>
					{#each data.students as s}
						<option value={s.id}>{s.name}</option>
					{/each}
				</select>
			</div>

			<input type="hidden" name="sessionId" value={data.sessionId} />

			<div class="flex justify-center">
				<Button variant="create" className="py-3" type="submit" formaction="?/start">create</Button>
			</div>
		</form>
	{/if}
</div>