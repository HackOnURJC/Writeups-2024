import { firefox } from "playwright-firefox";

const USER = "admin";
const PASSWD = process.env.PASSWD ?? console.log("No password") ?? process.exit(1);

const sleep = async (msec) =>
  new Promise((resolve) => setTimeout(resolve, msec));

export const visit = async (chall_url, url) => {
  console.log(chall_url)
  if (!/^https?:\/\/hackon-[a-f0-9]{12}-guglu-[0-9]+\.chals\.io\/$/.test(chall_url)) {
    console.log("Bad chall url");
    return;
  }

  console.log(`chall_url: ${chall_url}`)
  console.log(`url: ${url}`);

  const browser = await firefox.launch({
    headless: true,
    firefoxUserPrefs: {
      "javascript.options.wasm": false,
      "javascript.options.baselinejit": false,
    },
  });

  const context = await browser.newContext();

  try {
    const page = await context.newPage();

    await page.goto(chall_url + 'login', { timeout: 3 * 1000 });
    
    await page.type('input[name=username]', USER);
    await page.type('input[name=password]', PASSWD);
    await page.getByRole('button').click();

    await sleep(3 * 1000);

    await page.goto(url, { timeout: 3 * 1000 });
    await sleep(60 * 1000);
    await page.close();
  } catch (e) {
    console.error(e);
  }

  await browser.close();

  console.log(`end: ${url}`);
};