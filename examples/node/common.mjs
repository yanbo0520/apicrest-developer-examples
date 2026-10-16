// Local-only helpers; importing this module never calls an API.
export const BASE_URL = 'https://api.vv666.ai';

export function requireExecution(args = process.argv.slice(2), env = process.env) {
  if (!args.includes('--run')) {
    throw new Error('Dry by default: add --run only after reviewing live pricing and permissions.');
  }
  const key = (env.APICREST_API_KEY || '').trim();
  if (!key || ['YOUR_API_KEY', 'YOUR_REAL_API_KEY', 'REPLACE_WITH_YOUR_OWN_KEY'].includes(key)) {
    throw new Error('Set APICREST_API_KEY to your private key in the environment.');
  }
  return key;
}

export function classifyMediaJob(job) {
  if (!job || typeof job !== 'object') return 'unknown';
  if (job.state === 'success' && job.is_final === true) return 'success';
  if (job.state === 'failed' && job.is_final === true) return 'failed';
  if (['pending', 'running'].includes(job.state) && job.is_final !== true) return 'pending';
  return 'unknown';
}

export function argValue(name, fallback) {
  const i = process.argv.indexOf(name);
  return i === -1 ? fallback : process.argv[i + 1];
}

export async function checkedJson(response) {
  if (!response.ok) {
    let taskId;
    try { taskId = (await response.json())?.error?.task_id; } catch { /* ignore */ }
    if (taskId) console.error('Task ID for lookup:', taskId);
    throw new Error(`HTTP ${response.status}; submission is not retried.`);
  }
  return response.json();
}
