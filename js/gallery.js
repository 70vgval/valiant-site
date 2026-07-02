/* Gallery lightbox */

const GALLERY_DATA = [
  { title: 'VH Charger R/T E49', desc: 'The ultimate homologation special. 302 bhp from the 4.3L Hemi-6.', cls: 'gv-orange' },
  { title: 'VE Valiant Regal', desc: '1967 Wheels Car of the Year in True Blue metallic.', cls: 'gv-blue' },
  { title: 'VG Pacer', desc: 'Hemi-6 powered performance sedan with bold side stripes.', cls: 'gv-green' },
  { title: 'AP6 Wayfarer', desc: 'The uniquely Australian utility body on the AP6 platform.', cls: 'gv-mustard' },
  { title: 'CL Drifter Van', desc: 'Panel van variant of the CL generation — workhorse style.', cls: 'gv-cream' },
  { title: 'VJ Charger E55', desc: '340 cubic inch V8 — American muscle in Australian sheet metal.', cls: 'gv-orange' },
  { title: 'Chrysler by Chrysler', desc: 'Long-wheelbase luxury for the executive class.', cls: 'gv-black' },
  { title: 'CM Valiant Regal', desc: 'The final Australian Valiant, 1979–1981.', cls: 'gv-blue' },
];

document.addEventListener('DOMContentLoaded', () => {
  const grid = document.getElementById('gallery-grid');
  const lightbox = document.getElementById('lightbox');
  if (!grid) return;

  GALLERY_DATA.forEach((item, i) => {
    const el = document.createElement('div');
    el.className = 'gallery-item';
    el.innerHTML = `
      <div class="gallery-item__visual ${item.cls}">
        <span class="gallery-item__label">${item.title}</span>
      </div>
      <div class="gallery-item__overlay"></div>
    `;
    el.addEventListener('click', () => openLightbox(item));
    grid.appendChild(el);
  });

  function openLightbox(item) {
    if (!lightbox) return;
    lightbox.querySelector('.lightbox__title').textContent = item.title;
    lightbox.querySelector('.lightbox__desc').textContent = item.desc;
    lightbox.querySelector('.lightbox__visual').className = `lightbox__visual ${item.cls}`;
    lightbox.classList.add('active');
  }

  const closeBtn = lightbox?.querySelector('.lightbox__close');
  closeBtn?.addEventListener('click', () => lightbox.classList.remove('active'));
  lightbox?.addEventListener('click', (e) => {
    if (e.target === lightbox) lightbox.classList.remove('active');
  });
});
