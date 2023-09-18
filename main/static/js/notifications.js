isOpen = false;

async function toggleNotifications() {
  let notWindow = document.getElementById("notifications");
  let html = "<ul style='padding: 0'>";
  if (isOpen === false) {
    notWindow.style.display = "initial";
    isOpen = !isOpen;
  } else {
    notWindow.style.display = "none";
    isOpen = !isOpen;
    return;
  }
  // return;
  const res = await fetch(
    "/inbox/notifications/api/unread_list/?mark_as_read=true"
  );
  const nots = await res.json();
  notifications = nots.unread_list;
  notifications.map((notif) => {
    html += `<li><b>${notif.actor}</b> ${notif.verb} - ${notif.timestamp}</li>`;
  });
  html += "</ul>";
  html +=
    "<a style='color: inherit' href='/inbox/notifications/'>See all notifications.</a>";
  notWindow.innerHTML = html;
}
