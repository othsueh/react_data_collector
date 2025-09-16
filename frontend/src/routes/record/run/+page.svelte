<script lang="ts">
    import { Button } from '$lib';
    let { data } = $props();
  
    // Snapshot on first render; ignore later client load changes
    let hasCurrent = $state<boolean>(!!data.hasCurrent);
    let sessionId = $state<number | null>(data.sessionId ?? null);
    let studentId = $state<number | null>(data.studentId ?? null);
    let studentSessionId = $state<string>(data.studentSessionId ?? '');
    let studentName = $state<string>(data.studentName ?? '');
    let n_cycles = $state<number>(data.n_cycles ?? 0);
  
    let count = $state(0);
    let result = $state<number[]>([]);
    let stage = $state<'record' | 'final'>('record');
    let goals = $state(0);
  
    function push(val: number) {
      if (!hasCurrent || stage !== 'record') return;
      if (count >= n_cycles) return;
      result = [...result, val];
      count = result.length;
      if (count >= n_cycles) stage = 'final';
    }
  </script>
  
  {#if !hasCurrent}
  <div class="min-h-screen bg-white flex flex-col items-center mt-24 px-4">
    <h2 class="text-theme font-bold italic text-t2 text-center">record</h2>
    <p class="text-label text-xl mt-8">No active student session. <a href="/record" class="underline">Back</a></p>
  </div>
  {:else}
  <div class="min-h-screen bg-white flex flex-col items-center mt-24 md:mt-24 px-4">
    <h2 class="text-theme font-bold italic text-t2 text-center">record</h2>
    <div class="flex flex-col items-center mb-5">
      <svg width="192" height="8" class="mb-1"><rect x="0" y="0" width="192" height="6" class="fill-theme"/></svg>
      <svg width="192" height="8"><rect x="0" y="0" width="192" height="6" class="fill-theme"/></svg>
    </div>
  
    <div class="w-full flex flex-col items-center max-w-md space-y-2 text-label text-hl font-bold mb-5">
      <p>擊球者： {studentName}</p>
      <p>擊球數： {count} / {n_cycles}</p>
    </div>
  
    {#if stage === 'record'}
      <div class="w-full max-w-xs space-y-4">
        <button class="w-full rounded-3xl py-16 font-bold text-white text-t2 bg-blue-500" onclick={() => push(1)}>打 / 不接</button>
        <button class="w-full rounded-3xl py-16 font-bold text-white text-t2 bg-pink-500" onclick={() => push(0)}>接 / 不打</button>
        <button class="w-full rounded-3xl py-16 font-bold text-white text-t2 bg-purple-600" onclick={() => push(-1)}>無法判定</button>
      </div>
    {:else}
      <form class="w-full max-w-xs space-y-5" method="POST">
        <input type="hidden" name="sessionId" value={sessionId ?? ''} />
        <input type="hidden" name="studentId" value={studentId ?? ''} />
        <input type="hidden" name="student_session_id" value={studentSessionId ?? ''} />
        <input type="hidden" name="hit_miss_array" value={JSON.stringify(result)} />
        <div class="flex items-center justify-between gap-6">
          <label for="goals" class="text-label text-hl font-bold">總進球數</label>
          <input id="goals" name="goals_scored" type="number" min="0" bind:value={goals}
            class="max-w-20 text-center border border-gray-400 rounded-xl px-2 py-1 text-hl" />
        </div>
        <div class="flex justify-center">
          <Button type="submit" variant="end" className="py-3" formaction="?/finish">finish</Button>
        </div>
      </form>
    {/if}
  </div>
  {/if}