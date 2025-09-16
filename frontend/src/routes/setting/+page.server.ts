import type { Actions, PageServerLoad } from './$types';
import { backendFetchServer as backendFetch } from '$lib/api.server';

export const load: PageServerLoad = async ({ fetch }) => {
  // Default values for "no active session" state
  const defaults = {
    sessionName: 'Default',
    ballsPerTurn: 15,
    classCode: 2025
  };

  try {
    const res = await backendFetch(fetch, '/sessions/current');
    const s = await res.json();
    return {
      inSession: true,
      currentId: s.id as number,
      sessionName: (s.name as string) ?? defaults.sessionName,
      ballsPerTurn: (s.n_cycles as number) ?? defaults.ballsPerTurn,
      classCode: (s.class_type as string | number) ?? defaults.classCode
    };
  } catch {
    return {
      inSession: false,
      currentId: null,
      ...defaults
    };
  }
};

export const actions: Actions = {
  // Create a new session and let SvelteKit reload the page (which will detect in-session)
  create: async ({ fetch, request }) => {
    const fd = await request.formData();
    const payload = {
      name: String(fd.get('sessionName') ?? 'Default'),
      n_cycles: Number(fd.get('ballsPerTurn') ?? 15),
      class_type: String(fd.get('classCode') ?? '2322')
    };
    await backendFetch(fetch, '/sessions/', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
    return { success: true };
  },

  // Update current active session
  update: async ({ fetch, request }) => {
    const fd = await request.formData();
    const payload = {
      name: String(fd.get('sessionName') ?? ''),
      n_cycles: Number(fd.get('ballsPerTurn') ?? 0),
      class_type: String(fd.get('classCode') ?? '')
    };
    await backendFetch(fetch, '/sessions/current', {
      method: 'PUT',
      body: JSON.stringify(payload)
    });
    return { success: true };
  },

  // Deactivate current active session
  finish: async ({ fetch }) => {
    await backendFetch(fetch, '/sessions/current/deactivate', { method: 'PUT' });
    return { success: true };
  }
};