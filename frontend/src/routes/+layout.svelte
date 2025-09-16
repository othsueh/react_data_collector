<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { page } from '$app/stores';

	let { children } = $props();
	let mobileMenuOpen = $state(false);

	function toggleMobileMenu() {
		mobileMenuOpen = !mobileMenuOpen;
	}

	function closeMobileMenu() {
		mobileMenuOpen = false;
	}
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<!-- Navigation Bar -->
<nav class="bg-gray-100 px-4 py-3 flex justify-between items-center">
	<a href="/" class="text-theme font-bold text-t3">Reaction-C</a>
	
	<!-- Mobile menu button -->
	<button 
		onclick={toggleMobileMenu}
		class="text-theme md:hidden"
		aria-label="Toggle menu"
	>
		<svg class="w-8 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
		</svg>
	</button>

	<!-- Desktop menu -->
	<div class="hidden md:flex space-x-6">
		<a href="/setting" class="text-theme font-semibold italic hover:bg-gray-300 transition-colors">setting</a>
		<a href="/mrecord" class="text-theme font-semibold italic hover:bg-gray-300 transition-colors">mrecord</a>
		<a href="/record" class="text-theme font-semibold italic hover:bg-gray-300 transition-colors">record</a>
	</div>
</nav>

<!-- Mobile menu overlay -->
{#if mobileMenuOpen}
	<div class="fixed inset-0 bg-black bg-opacity-50 z-50 md:hidden" onclick={closeMobileMenu}>
		<div class="bg-gray-100 p-6 m-4 rounded-lg" onclick={(e) => e.stopPropagation()}>
			<div class="flex justify-between items-center mb-6">
				<h2 class="text-theme font-bold text-hl">Reaction-C</h2>
				<button onclick={closeMobileMenu} class="text-blue-600">
					<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
					</svg>
				</button>
			</div>
			
			<div class="space-y-4">
				<a href="/setting" onclick={closeMobileMenu} class="block font-semibold italic text-theme hover:bg-gray-500 transition-colors">setting</a>
				<a href="/mrecord" onclick={closeMobileMenu} class="block font-semibold italic text-theme hover:bg-gray-500 transition-colors">mrecord</a>
				<a href="/record" onclick={closeMobileMenu} class="block font-semibold italic text-theme hover:bg-gray-500 transition-colors">record</a>
				<a href="/stats" onclick={closeMobileMenu} class="block font-semibold italic text-theme hover:bg-gray-500 transition-colors">stats</a>
			</div>
		</div>
	</div>
{/if}

<!-- Main content -->
<main class="min-h-screen bg-white">
	{@render children?.()}
</main>