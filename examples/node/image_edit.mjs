// Node.js 20+; multipart upload. DO NOT auto retry this potentially billable POST.
import { readFile, writeFile, stat } from 'node:fs/promises';
import { extname, basename } from 'node:path';
import { BASE_URL, argValue, checkedJson, requireExecution } from './common.mjs';

async function main() {
  const key = requireExecution();
  const imagePath = argValue('--image');
  const outputPath = argValue('--out', 'edited-node.png');
  if (!imagePath) throw new Error('Pass --image ./product.png');
  const type = ({ '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg' })[extname(imagePath).toLowerCase()];
  if (!type) throw new Error('This example accepts only PNG or JPEG.');
  if ((await stat(imagePath)).size > 10 * 1024 * 1024) throw new Error('Local safety limit is 10 MiB.');

  const form = new FormData();
  form.append('model', process.env.APICREST_IMAGE_MODEL || 'gpt-image-2.5');
  form.append('prompt', 'Place the product on a wooden desk; preserve package details as closely as possible.');
  form.append('size', '1536x1024');
  form.append('quality', 'high');
  form.append('response_format', 'b64_json');
  form.append('image[]', new Blob([await readFile(imagePath)], { type }), basename(imagePath));

  let response;
  try {
    response = await fetch(`${BASE_URL}/v1/images/edits`, {
      method: 'POST', headers: { Authorization: `Bearer ${key}` },
      body: form, signal: AbortSignal.timeout(360_000),
    });
  } catch {
    throw new Error('Network/timeout: request outcome UNKNOWN. Reconcile tasks; do not retry POST blindly.');
  }
  const taskId = response.headers.get('X-Task-Id');
  if (taskId) console.log('Task ID for reconciliation:', taskId);
  const body = await checkedJson(response);
  const encoded = body?.data?.[0]?.b64_json;
  if (typeof encoded !== 'string' || !encoded) throw new Error('Unexpected image response; do not auto retry.');
  // Check alphabet to avoid silently accepting malformed data.
  if (!/^[A-Za-z0-9+/]+={0,2}$/.test(encoded)) throw new Error('Invalid base64 result.');
  await writeFile(outputPath, Buffer.from(encoded, 'base64'));
  console.log('Saved:', outputPath);
}

main().catch(err => { console.error(err.message); process.exitCode = 1; });
