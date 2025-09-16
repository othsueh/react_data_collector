import type { PageServerLoad, Actions } from './$types';
import { redirect } from '@sveltejs/kit';
import { backendFetchServer as backendFetch } from '$lib/api.server';

export const load: PageServerLoad = async ({ fetch }) => {
  try {
    const curStuRes = await backendFetch(fetch, '/student-sessions/current');
    const curStu = await curStuRes.json();
    if (!curStu) return { hasCurrent: false };

    const curSessionRes = await backendFetch(fetch, '/sessions/current');
    const curSession = await curSessionRes.json();

    const studentRes = await backendFetch(fetch, `/students/${curStu.student_id}`);
    const student = await studentRes.json();

    return {
      hasCurrent: true,
      sessionId: curStu.session_id as number,
      studentSessionId: curStu.student_session_uuid as string,
      studentId: curStu.student_id as number,
      studentName: student.name as string,
      n_cycles: curSession.n_cycles as number
    };
  } catch {
    return { hasCurrent: false };
  }
};

export const actions: Actions = {
  finish: async ({ fetch, request }) => {
    const fd = await request.formData();
    const session_id = Number(fd.get('sessionId'));
    const student_id = Number(fd.get('studentId'));
    const student_session_id = String(fd.get('student_session_id'));
    const hit_miss_array = JSON.parse(String(fd.get('hit_miss_array') || '[]')) as number[];
    const goals_scored = Number(fd.get('goals_scored') || 0);

    await backendFetch(fetch, '/student-records/', {
      method: 'POST',
      body: JSON.stringify({
        session_id,
        student_session_id,
        student_id,
        hit_miss_array,
        goals_scored
      })
    });

    // Deactivate current student session
    await backendFetch(fetch, '/student-sessions/current/deactivate', { method: 'PUT' });
    throw redirect(303,'/record')
  }
};