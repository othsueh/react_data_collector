import type { Actions, PageServerLoad } from './$types';
import { backendFetchServer as backendFetch } from '$lib/api.server';
import { redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ fetch, url }) => {
  const waitFor = url.searchParams.get('wait'); // studentSessionId to wait for
  try {
    const curStuRes = await backendFetch(fetch, '/student-sessions/current');
    const curStu = await curStuRes.json();
    if (!curStu) return { inStudentSession: false, waitFor };

    const sessionRes = await backendFetch(fetch, '/sessions/current');
    const session = await sessionRes.json();

    const studentRes = await backendFetch(fetch, `/students/${curStu.student_id}`);
    const student = await studentRes.json();

    return {
      inStudentSession: true,
      sessionId: session.id as number,
      studentSessionId: curStu.student_session_uuid as string,
      studentId: curStu.student_id as number,
      studentName: student.name as string,
      n_cycles: session.n_cycles as number,
      waitFor
    };
  } catch {
    return { inStudentSession: false, waitFor };
  }
};

export const actions: Actions = {
  submit: async ({ fetch, request }) => {
    const fd = await request.formData();
    const session_id = Number(fd.get('sessionId'));
    const student_id = Number(fd.get('studentId'));
    const student_session_id = String(fd.get('studentSessionId'));
    const hit_miss_array = JSON.parse(String(fd.get('hit_miss_array') || '[]')) as number[];

    await backendFetch(fetch, '/machine-records/', {
      method: 'POST',
      body: JSON.stringify({ session_id, student_session_id, student_id, hit_miss_array })
    });

    // Redirect back with wait token
    throw redirect(303, `/mrecord?wait=${encodeURIComponent(student_session_id)}`);
  }
};