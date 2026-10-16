// Node.js 20+; one async submission, bounded polling. Requires --run.
import { setTimeout as sleep } from 'node:timers/promises';
import { BASE_URL, checkedJson, classifyMediaJob, requireExecution } from './common.mjs';

async function main() {
  const key = requireExecution();
  const headers = { Authorization: `Bearer ${key}` };
  let created;
  try {
    const response = await fetch(`${BASE_URL}/v1/media/generate`, {
      method: 'POST', headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: process.env.APICREST_IMAGE_MODEL || 'gpt-image-2.5',
        prompt: 'A small robot watering a bonsai tree, studio lighting.',
        params: { aspect_ratio: '1:1', quality: 'auto' },
      }),
      signal: AbortSignal.timeout(30_000),
    });
    created = await checkedJson(response);
  } catch (err) {
    throw new Error(`Submission result unknown. Do not auto-retry POST. ${err.message}`);
  }
  const taskId = created?.task_id;
  if (!taskId || typeof taskId !== 'string') throw new Error('No task_id. Reconcile account activity before retry.');
  console.log('Save task ID:', taskId);

  const deadline = Date.now() + 10 * 60_000;
  while (Date.now() < deadline) {
    await sleep(8_000);
    let job;
    try {
      const query = new URLSearchParams({ task_id: taskId });
      const response = await fetch(`${BASE_URL}/v1/media/status?${query}`, {
        headers, signal: AbortSignal.timeout(30_000),
      });
      job = await checkedJson(response);
    } catch {
      console.error('Status lookup failed; task ID retained. Check later instead of resubmitting.');
      return;
    }
    const outcome = classifyMediaJob(job);
    if (outcome === 'success') { console.log('Result URL:', job.result_url || '(none returned)'); return; }
    if (outcome === 'failed') { console.log('Task failed. Reconcile status/cost with task ID:', taskId); return; }
    if (outcome === 'unknown') { console.log('Unexpected state; consult docs for ID:', taskId); return; }
    console.log('Pending:', taskId);
  }
  console.log('Polling deadline reached; task might continue. Keep ID:', taskId);
}

main().catch(err => { console.error(err.message); process.exitCode = 1; });
