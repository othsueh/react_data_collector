<script lang="ts">
	let { data } = $props();
</script>

<div class="mt-24 flex min-h-screen flex-col items-center bg-white px-4 md:mt-24">
	<h2 class="text-theme text-t2 text-center font-bold italic">stats</h2>
	<div class="mb-8 flex flex-col items-center">
		<svg width="192" height="8" class="mb-1"
			><rect x="0" y="0" width="192" height="6" class="fill-theme" /></svg
		>
		<svg width="192" height="8"><rect x="0" y="0" width="192" height="6" class="fill-theme" /></svg>
	</div>

	{#if !data.inSession}
		<div class="text-label text-t3 mt-8 space-y-8 text-center font-bold italic">
			<div>
				<p>Not</p>
				<p>In A</p>
				<p>Session</p>
			</div>
		</div>
	{:else}
		<div class="w-full max-w-4xl overflow-x-auto">
			<table class="w-full border-collapse">
				<thead>
					<tr class="text-label text-hl text-left">
						<th class="border-b px-3 py-2">Student</th>
						<th class="border-b px-3 py-2">Time</th>
						<th class="border-b px-3 py-2">mrecord</th>
						<th class="border-b px-3 py-2">record</th>
					</tr>
				</thead>
				<tbody>
					{#each data.rows as r}
						<tr class="text-lg">
							<td class="border-b px-3 py-2">{r.studentName}</td>
							<td class="border-b px-3 py-2 text-sm">{new Date(r.createdAt).toLocaleString()}</td>
							<td class="border-b px-3 py-2">{r.hasM ? '✅' : '❌'}</td>
							<td class="border-b px-3 py-2">{r.hasS ? '✅' : '❌'}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	{/if}
</div>
