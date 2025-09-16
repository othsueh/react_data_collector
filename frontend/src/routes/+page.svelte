<script lang="ts">
	import { goto } from '$app/navigation';
	import { Button } from '$lib';
</script>

<div class="min-h-screen bg-white flex flex-col items-center mt-24 px-4">
	<!-- Main title -->
	<div class="text-center mb-8">
		<h1 class="text-theme font-bold italic text-t1 md:text-t1">Reaction-C</h1>
		
		<!-- Decorative lines SVG -->
		<div class="flex-row justify-center mb-4.5">
			<svg width="280" height="8" class="mb-0.5">
				<rect x="0" y="0" width="140" height="6" rx="4" class="fill-theme"/>
			</svg>
			<svg width="280" height="8" class="mb-0.5">
				<rect x="63" y="0" width="140" height="6" rx="4" class="fill-theme"/>
			</svg>
			<svg width="280" height="8">
				<rect x="111" y="0" width="140" height="6" rx="4" class="fill-theme"/>
			</svg>
		</div>
		
		<!-- Description -->
		<div class="text-theme italic text-lg md:text-xl">
			<p>The web app designed for</p>
			<p>collecting</p>
			<p>Ping-Pong reaction data</p>
		</div>
	</div>

	<!-- Action buttons -->
	<div class="space-y-4 w-48 max-w-sm">
		<Button variant="label" className="font-medium" onclick={() => goto('/setting')}>setting</Button>
		<Button variant="create" onclick={() => goto('/mrecord')}>mrecord</Button>
		<Button variant="end" onclick={() => goto('/record')}>record</Button>
	</div>
</div>