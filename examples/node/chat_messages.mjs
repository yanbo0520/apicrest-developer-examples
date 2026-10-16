// Node.js 20+; one potentially billable request only with --run.
import { BASE_URL, checkedJson, requireExecution } from './common.mjs';

async function main() {
  const key = requireExecution();
  const response = await fetch(`${BASE_URL}/v1/messages`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: process.env.APICREST_CHAT_MODEL || 'claude-haiku-5-5',
      max_tokens: 256,
      messages: [{ role: 'user', content: 'Explain idempotency in two sentences.' }],
    }),
    signal: AbortSignal.timeout(60_000),
  });
  const data = await checkedJson(response);
  const text = (data.content || []).filter(b => b.type === 'text').map(b => b.text).join('\n');
  console.log(text);
}

main().catch(err => { console.error(err.message); process.exitCode = 1; });
