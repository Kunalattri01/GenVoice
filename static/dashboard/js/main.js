// ---------- Sidebar toggle (mobile) ----------
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebarOverlay = document.getElementById('sidebarOverlay');

function openSidebar() {
    sidebar.classList.add('sidebar-open');
    sidebarOverlay.classList.remove('hidden');
}
function closeSidebar() {
    sidebar.classList.remove('sidebar-open');
    sidebarOverlay.classList.add('hidden');
}

sidebarToggle.addEventListener('click', () => {
    sidebar.classList.contains('sidebar-open') ? closeSidebar() : openSidebar();
});
sidebarOverlay.addEventListener('click', closeSidebar);

// Close sidebar on nav link click (mobile)
document.querySelectorAll('#sidebarNav .nav-link').forEach(link => {
    link.addEventListener('click', () => {
    if (window.innerWidth < 1024) closeSidebar();
    });
});

// ---------- Generic dropdown handling ----------
function setupDropdown(btnId, dropdownId) {
    const btn = document.getElementById(btnId);
    const dropdown = document.getElementById(dropdownId);

    btn.addEventListener('click', (e) => {
    e.stopPropagation();
    const isOpen = !dropdown.classList.contains('hidden');
    closeAllDropdowns();
    if (!isOpen) dropdown.classList.remove('hidden');
    });

    dropdown.addEventListener('click', (e) => e.stopPropagation());
}

function closeAllDropdowns() {
    document.getElementById('notifDropdown').classList.add('hidden');
    document.getElementById('msgDropdown').classList.add('hidden');
    document.getElementById('profileDropdown').classList.add('hidden');
}

setupDropdown('notifBtn', 'notifDropdown');
setupDropdown('msgBtn', 'msgDropdown');
setupDropdown('profileBtn', 'profileDropdown');

document.addEventListener('click', closeAllDropdowns);
window.addEventListener('resize', () => {
    if (window.innerWidth >= 1024) closeSidebar();
});