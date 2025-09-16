import type { Actions, PageServerLoad } from './$types';
import { backendFetchServer as backendFetch } from '$lib/api.server';
import { redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ fetch }) => {
  const curStu = await (await backendFetch(fetch, '/student-sessions/current')).json();
  if (curStu) throw redirect(303, '/record/run');

  try {
    const curRes = await backendFetch(fetch, '/sessions/current');
    const current = await curRes.json();

    const stuRes = await backendFetch(fetch, `/sessions/${current.id}/students`);
    const students = await stuRes.json();

    return {
      inSession: true,
      sessionId: current.id as number,
      n_cycles: current.n_cycles as number,
      students: students.map((s: any) => ({ id: s.id as number, name: s.name as string }))
    };
  } catch {
    return { inSession: false, sessionId: null, n_cycles: 0, students: [] };
  }
};

export const actions: Actions = {
  start: async ({ fetch, request }) => {
    const fd = await request.formData();
    const session_id = Number(fd.get('sessionId'));
    const student_id = Number(fd.get('studentId'));
    await backendFetch(fetch, '/student-sessions/', {
      method: 'POST',
      body: JSON.stringify({ session_id, student_id })
    });
    throw redirect(303, '/record/run');
  }
};