/* Interactive model timeline */

const VALIANT_MODELS = [
  {
    era: 'First Generation',
    years: '1962–1963',
    model: 'RV1 – R Series',
    year: 1962,
    gen: 1,
    detail: 'The first Australian-built Valiant, assembled at Tonsley Park from CKD kits. Featured the Slant-6 engine and established Chrysler\'s local manufacturing presence.',
    variants: ['Sedan'],
  },
  {
    era: 'First Generation',
    years: '1962–1963',
    model: 'SV1 – S Series',
    year: 1962,
    gen: 1,
    detail: 'Updated styling with a new grille and trim options. Sold alongside the R Series as Chrysler refined its Australian offering.',
    variants: ['Sedan'],
  },
  {
    era: 'Second Generation',
    years: '1963',
    model: 'AP5',
    year: 1963,
    gen: 2,
    detail: 'First fully Australian-designed Valiant body. Available as sedan and Safari wagon, marking a major step toward local identity.',
    variants: ['Sedan', 'Safari Wagon'],
  },
  {
    era: 'Second Generation',
    years: '1965',
    model: 'AP6',
    year: 1965,
    gen: 2,
    detail: 'Refined AP5 with improved trim and the introduction of the Wayfarer utility — a uniquely Australian body style.',
    variants: ['Sedan', 'Safari Wagon', 'Wayfarer Ute'],
  },
  {
    era: 'Second Generation',
    years: '1966',
    model: 'VC',
    year: 1966,
    gen: 2,
    detail: 'Sharper styling with stacked headlights. The VC Valiant brought a more aggressive, modern look to the range.',
    variants: ['Sedan', 'Safari Wagon', 'Wayfarer Ute', 'Regal Safari'],
  },
  {
    era: 'Third Generation',
    years: '1967',
    model: 'VE',
    year: 1967,
    gen: 3,
    detail: 'Wheels magazine Car of the Year. Wider body, improved handling, and the introduction of the VIP luxury trim line.',
    variants: ['Sedan', 'Safari Wagon', 'VIP'],
    highlight: 'Car of the Year',
  },
  {
    era: 'Third Generation',
    years: '1969',
    model: 'VF',
    year: 1969,
    gen: 3,
    detail: 'More luxury and performance options. The VF range expanded trim levels and introduced greater personalisation.',
    variants: ['Sedan', 'Safari Wagon', 'VIP', 'Regal'],
  },
  {
    era: 'Third Generation',
    years: '1970',
    model: 'VG',
    year: 1970,
    gen: 3,
    detail: 'Historic introduction of the Australian-designed Hemi-6 engine — a straight-six that would become legendary.',
    variants: ['Sedan', 'Safari Wagon', 'Pacer', 'Regal'],
    highlight: 'Hemi-6 Debut',
  },
  {
    era: 'Fourth Generation',
    years: '1971',
    model: 'VH',
    year: 1971,
    gen: 4,
    detail: 'The generation that gave Australia the Charger. Bold fastback styling and the birth of "Hey Charger!" marketing.',
    variants: ['Sedan', 'Charger', 'Charger XL', 'Charger 770', 'R/T E38', 'R/T E49'],
    highlight: 'Hey Charger!',
  },
  {
    era: 'Fourth Generation',
    years: '1973',
    model: 'VJ',
    year: 1973,
    gen: 4,
    detail: 'Refined VH platform with the E55 340 V8 Charger — American muscle meets Australian engineering.',
    variants: ['Sedan', 'Charger', 'Charger 770', 'E55 340 V8'],
    highlight: 'E55 340 V8',
  },
  {
    era: 'Fifth Generation',
    years: '1975',
    model: 'VK',
    year: 1975,
    gen: 5,
    detail: 'Shift toward comfort and refinement. Updated styling with a focus on ride quality and interior appointments.',
    variants: ['Sedan', 'Charger', 'Regal'],
  },
  {
    era: 'Fifth Generation',
    years: '1976',
    model: 'CL',
    year: 1976,
    gen: 5,
    detail: 'Introduced the Drifter panel van and ute. The Charger 770 continued as the performance flagship.',
    variants: ['Sedan', 'Charger 770', 'Drifter Van', 'Drifter Ute'],
  },
  {
    era: 'Final Generation',
    years: '1979–1981',
    model: 'CM',
    year: 1979,
    gen: 6,
    detail: 'The last Australian-built Valiant. Production ended in 1981, closing a remarkable chapter of local motoring.',
    variants: ['Sedan', 'Regal', 'Sigma-based variants'],
    highlight: 'Final Model',
  },
  {
    era: 'Luxury & Special',
    years: '1965–1971',
    model: 'Chrysler by Chrysler',
    year: 1965,
    gen: 0,
    detail: 'Long-wheelbase luxury sedans (CH, CJ, CK) built for the executive market. Australian prestige motoring at its finest.',
    variants: ['CH', 'CJ', 'CK'],
  },
];

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('timeline-container');
  const filters = document.querySelectorAll('.filter-btn');
  if (!container) return;

  let activeGen = 'all';

  function render(gen) {
    container.innerHTML = '';
    const filtered = gen === 'all' ? VALIANT_MODELS : VALIANT_MODELS.filter((m) => m.gen === parseInt(gen, 10));

    filtered.forEach((model, i) => {
      const item = document.createElement('div');
      item.className = 'timeline__item';
      item.dataset.index = i;

      const highlight = model.highlight
        ? `<span class="badge badge--mustard">${model.highlight}</span>`
        : '';

      const variants = model.variants
        .map((v) => `<span class="badge badge--orange">${v}</span>`)
        .join('');

      item.innerHTML = `
        <div class="timeline__era">${model.era} · ${model.years}</div>
        <div class="timeline__model">${model.model}</div>
        ${highlight}
        <div class="timeline__detail">
          <p class="card__body">${model.detail}</p>
          <div class="timeline__variants">${variants}</div>
        </div>
      `;

      item.addEventListener('click', () => {
        const wasActive = item.classList.contains('active');
        container.querySelectorAll('.timeline__item').forEach((el) => {
          el.classList.remove('active', 'dimmed');
        });
        if (!wasActive) {
          item.classList.add('active');
          container.querySelectorAll('.timeline__item').forEach((el) => {
            if (el !== item) el.classList.add('dimmed');
          });
        }
      });

      container.appendChild(item);
    });
  }

  filters.forEach((btn) => {
    btn.addEventListener('click', () => {
      filters.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      activeGen = btn.dataset.gen;
      render(activeGen);
    });
  });

  render(activeGen);
});
