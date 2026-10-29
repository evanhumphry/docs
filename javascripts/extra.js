const setupChecklist = () => {
  const taskLists = document.querySelectorAll(".md-content .task-list");
  if (!taskLists.length || document.querySelector(".checklist-progress")) return;

  const pageKey = `task-list:${window.location.pathname}`;
  const checkboxes = [...document.querySelectorAll(
    ".md-content .task-list-item input[type='checkbox']"
  )];

  if (!checkboxes.length) return;

  let saved = {};
  try {
    saved = JSON.parse(localStorage.getItem(pageKey) || "{}");
  } catch {
    localStorage.removeItem(pageKey);
  }
  const checklist = document.createElement("section");
  checklist.className = "checklist-progress";
  checklist.setAttribute("aria-label", "Checklist progress");
  checklist.innerHTML = `
    <div class="checklist-progress__summary">
      <strong>Progress</strong>
      <span data-checklist-count></span>
    </div>
    <progress max="${checkboxes.length}" value="0"></progress>
    <button type="button" class="md-button" data-checklist-reset>Reset checklist</button>
  `;

  taskLists[0].before(checklist);
  const count = checklist.querySelector("[data-checklist-count]");
  const progress = checklist.querySelector("progress");

  const updateProgress = () => {
    const completed = checkboxes.filter((checkbox) => checkbox.checked).length;
    count.textContent = `${completed} of ${checkboxes.length} complete`;
    progress.value = completed;
  };

  checkboxes.forEach((checkbox, index) => {
    checkbox.disabled = false;
    checkbox.checked = saved[index] === true;
    checkbox.setAttribute("aria-label", checkbox.closest(".task-list-item").textContent.trim());
    checkbox.addEventListener("change", () => {
      saved[index] = checkbox.checked;
      localStorage.setItem(pageKey, JSON.stringify(saved));
      updateProgress();
    });
  });

  checklist.querySelector("[data-checklist-reset]").addEventListener("click", () => {
    if (!window.confirm("Reset all checkboxes on this page?")) return;
    checkboxes.forEach((checkbox) => { checkbox.checked = false; });
    localStorage.removeItem(pageKey);
    Object.keys(saved).forEach((key) => delete saved[key]);
    updateProgress();
  });

  updateProgress();
};

if (typeof document$ !== "undefined") {
  document$.subscribe(setupChecklist);
} else if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", setupChecklist, { once: true });
} else {
  setupChecklist();
}
