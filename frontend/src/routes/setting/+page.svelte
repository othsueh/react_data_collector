<script lang="ts">
	import { Button } from '$lib';
	let { data } = $props();
  
	let inSession = $state(!!data.inSession);
	let sessionName = $state<string>(data.sessionName);
	let ballsPerTurn = $state<number>(data.ballsPerTurn);
	let classCode = $state<string | number>(data.classCode);
  
	// When the server actions complete, the page reloads and `data` updates,
	// so mirror those changes into local state.
	$effect(() => {
	  inSession = !!data.inSession;
	  sessionName = data.sessionName;
	  ballsPerTurn = data.ballsPerTurn;
	  classCode = data.classCode;
	});
  </script>
  
  <div class="min-h-screen bg-white flex flex-col items-center mt-24 md:mt-24 px-4">
	<h2 class="text-theme font-bold italic text-t2 text-center">Setting</h2>
	<div class="flex flex-col items-center mb-12">
	  <svg width="192" height="8" class="mb-1"><rect x="0" y="0" width="192" height="6" class="fill-theme"/></svg>
	  <svg width="192" height="8"><rect x="0" y="0" width="192" height="6" class="fill-theme"/></svg>
	</div>
  
	<form class="w-full max-w-md space-y-8" method="POST">
	  <div>
		<label for="sessionName" class="block text-label text-hl font-bold mb-3">session name</label>
		<input
		  id="sessionName"
		  name="sessionName"
		  type="text"
		  placeholder="Default"
		  bind:value={sessionName}
		  class="w-full border border-gray-400 rounded-xl px-2 py-1 text-hl focus:outline-none focus:ring-2 focus:ring-theme"
		/>
	  </div>
  
	  <div class="flex items-center justify-between gap-4">
		<label for="ballsPerTurn" class="text-label text-hl font-bold"># of balls / turn</label>
		<input
		  id="ballsPerTurn"
		  name="ballsPerTurn"
		  type="number"
		  min="1"
		  max="99"
		  inputmode="numeric"
		  bind:value={ballsPerTurn}
		  class="max-w-20 text-center border border-gray-400 rounded-xl px-2 py-1 text-hl"
		/>
	  </div>
  
	  <div class="flex items-center justify-between gap-4">
		<label for="classCode" class="text-label text-hl font-bold">which class</label>
		<input
		  id="classCode"
		  name="classCode"
		  type="text"
		  bind:value={classCode}
		  class="max-w-28 text-center border border-gray-400 rounded-xl px-2 py-1 text-hl"
		/>
	  </div>
  
	  {#if inSession}
		<div class="mt-8 w-full flex flex-col items-center gap-4">
		  <Button type="submit" variant="start" className="py-3" formaction="?/update">update</Button>
		  <Button type="submit" variant="end" className="py-3" formaction="?/finish">finish</Button>
		</div>
	  {:else}
		<div class="mt-8 w-full flex justify-center">
		  <Button type="submit" variant="create" className="py-3" formaction="?/create">create</Button>
		</div>
	  {/if}
	</form>
  </div>