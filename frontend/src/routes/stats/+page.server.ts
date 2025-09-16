import type { PageServerLoad } from './$types';
import { backendFetchServer as backendFetch } from '$lib/api.server';

type Row = { 
  studentSessionId: string; 
  studentId: number; 
  studentName: string; 
  createdAt: string;
  hasM: boolean; 
  hasS: boolean 
};

export const load: PageServerLoad = async ({ fetch }) => {
  // get current session
  const current = await backendFetch(fetch, '/sessions/current').then(r => r.json()).catch(() => null);
  if (!current) {
    return { inSession: false, rows: [] as Row[] };
  }

  // get all student sessions for this session
  const studentSessions = await backendFetch(fetch, `/student-sessions/session/${current.id}`).then(r => r.json());

  // get students lookup
  const students = await backendFetch(fetch, `/sessions/${current.id}/students`).then(r => r.json());
  const studentMap = new Map(students.map((s: any) => [s.id, s.name]));

  // get records
  const mrecords = await backendFetch(fetch, `/machine-records/session/${current.id}`).then(r => r.json());
  const srecords = await backendFetch(fetch, `/student-records/session/${current.id}`).then(r => r.json());

  // build lookups by student_session_id
  const mBySS = new Set(mrecords.map((m: any) => m.student_session_id));
  const sBySS = new Set(srecords.map((s: any) => s.student_session_id));

  const rows: Row[] = studentSessions.map((ss: any) => ({
    studentSessionId: ss.student_session_uuid as string,
    studentId: ss.student_id as number,
    studentName: studentMap.get(ss.student_id) || 'Unknown',
    createdAt: ss.created_at as string,
    hasM: mBySS.has(ss.student_session_uuid),
    hasS: sBySS.has(ss.student_session_uuid)
  }));

  // sort by creation time (reverse)
  rows.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());

  return {
    inSession: true,
    sessionId: current.id as number,
    rows
  };
};