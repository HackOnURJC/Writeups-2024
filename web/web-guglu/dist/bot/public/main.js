const $ = document.getElementById.bind(document);

let loading = false;
$("report").addEventListener("click", async () => {
  if (loading) return;
  const chall_url = $("chall_url").value;
  if (!chall_url.match("^https?://hackon-[a-f0-9]{12}-guglu-[0-9]+\.chals\.io/$")) {
    alert("Invalid chall url");
    return;
  }
  const url = $("url").value;
  if (!url.startsWith("http://") && !url.startsWith("https://")) {
    alert("Invalid url");
    return;
  }

  loading = true;
  $("report").toggleAttribute("disabled");
  $("report").setAttribute("aria-busy", "true");
  $("report").textContent = "";

  const res = await fetch("/api/report", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url, chall_url }),
  });
  if (res.status === 200) {
    alert("Completed!");
  } else {
    alert(await res.text());
  }

  loading = false;
  $("report").toggleAttribute("disabled");
  $("report").setAttribute("aria-busy", "false");
  $("report").textContent = "Report";
});
