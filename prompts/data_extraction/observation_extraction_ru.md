# Промпт для извлечения одной observation

Версия: 0.2 от 2026-09-05

Извлекай сведения только из предоставленного и фактически прочитанного источника.
Одна observation — один результат одного свойства в одном физическом контексте.

Перед работой прочитай:

- `data/schemas/observation.schema.json`;
- `metadata/vocabularies/property_terms.csv`;
- `docs/decisions/0002_property_taxonomy.md`;
- `docs/methods/evidence_review_protocol.md`.

Создай два отдельных файла.

## 1. observation.json

Верни только JSON, строго совместимый со схемой. Не добавляй полей, которых в ней нет.

- Сохрани `raw_value_text`, исходное число, единицу и basis без исправления.
- Каноническое значение укажи отдельно с правилом и версией преобразования.
- Зафиксируй всех участников контекста, а не только «фаза 1/фаза 2».
- Для liquid-liquid зафиксируй две разные жидкости и состав каждой фазы.
- Для contact angle зафиксируй каплю, окружающую фазу, поверхность,
  `measured_through_participant_id`, геометрию и подготовку поверхности.
- Для dynamic tension создай `series` с координатой `surface_age` и `time_origin`.
- Для МУНТ укажи физическую партию, basis концентрации, basis активного вещества,
  состав дисперсии и методический run. Характеристики МУНТ — отдельные observations.
- Выбирай методически конкретный `property_id`: не объединяй седиментацию с
  центрифугированием, DLS с image sizing, fitted yield stress с API yield point или
  удержание в пористой среде с доказанной адсорбцией. Generic ID оставляй только в
  staging, когда источник не позволяет более точную классификацию.
- Для нормированных долей и нагрузок укажи `measurand_entity_id` и `result_basis`.
  Для центрифугирования обязательны RCF, длительность и определение supernatant.
- Не классифицируй сверхкритический флюид как газовую фазу для surface tension;
  помести такую запись в quarantine до утверждения отдельного контекста.
- Разделяй научное происхождение результата (`origin_kind`) и путь получения записи
  (`ingestion_route`).
- Для машинного извлечения укажи в `source_assertion` значения
  `extraction_mode=machine` и `verification_status=machine_extracted`; не выдавай
  машинную запись за проверенную человеком.
- Если температура или другое условие не приведено, создай condition со статусом
  `not_reported`, причиной и флагом quarantine; не подставляй 298.15 K.
- Любая отсутствующая uncertainty должна быть явным компонентом со статусом
  `not_reported`.
- Все результаты модели имеют `quality.data_level=staging` и
  `quality.review_status=machine_extracted`.

## 2. audit.json

Этот файл не является частью observation schema. Верни:

```json
{
  "observation_id": "...",
  "source_locator": "page/table/figure/row or database record ID",
  "verification_excerpt_max_20_words": "...",
  "missing_fields": [],
  "ambiguities": [],
  "digitization_required": false,
  "potential_duplicate_ids": [],
  "human_review_priority": "high|medium|low"
}
```

Фрагмент нужен только для внутренней проверки и не должен превышать 20 слов.

## Запрещено

- угадывать условия, составы, неопределённости, DOI или номера страниц;
- считать общий номинальный состав равновесным составом обеих фаз;
- смешивать surface tension, IFT, contact angle, adsorption и drilling endpoints;
- считать experiment, MD, QM, CFD и ML взаимозаменяемыми evidence;
- выдавать точку с графика за точное табличное значение;
- трактовать `ppb` как parts per billion без подтверждения контекста;
- объединять два результата, например IFT и вязкость, в одну observation;
- повышать запись до `curated` или `model_ready`.

Если критично неясны property ID, участники контекста, единица, basis концентрации или
локатор, всё равно сохрани source-native staging-запись только когда схема это позволяет,
поставь флаг `quarantine` и подробно перечисли проблему в `audit.json`. Если корректную
запись создать невозможно, не выдумывай поля: верни только `audit.json` с причиной.
