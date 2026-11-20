# FREP — исправления утреннего отчёта

19.11.2026. Замечания из [REPORT-CHECK.md](REPORT-CHECK.md) сверены с результатами и указанными ниже свидетельствами. Новых опытов не было.

1. **Исправлено: X1/X1C — ? / ? / ?.** В [X/X1C-RESULT.md](../samples/arch-silverblue-freebsd/X1C-RESULT.md), раздел «Application of §9.2», три нуля выведены только из расхождения классификаций; доказательство двух классов прямо не заявлено. На решающих строках `.inputrc`, `.bashrc`, `.exrc` стоят `hole-none` и `data`. Неизвестный класс не является другим классом по [PAPER.html §9.2](../../first-paper/PAPER.html). Это подтверждает и [X/REVIEW-X1C.md](../samples/arch-silverblue-freebsd/REVIEW-X1C.md), п. 5, хотя прежняя рецензия принимала нули. В REPORT прежние нули сняты; исходный X1C оставлен как историческая запись. Общий итог первой проверки остаётся **0** по A, V и W.

2. **Исправлено: абзац о методическом расхождении.** Убрано оправдание сохранения опубликованных оценок. Теперь прямо сказано, почему `hole-none` не даёт ноль. Та же трактовка есть в [X/X2C-RESULT.md](../samples/debian-desktop/X2C-RESULT.md) (8 строк `hole-none → data`, итог ?), [E/REVIEW-E6C.md](../samples/ubuntu-alpine/REVIEW-E6C.md), п. 2, P/REVIEW-P1-1-2.md, п. 2, и P/REVIEW-P2-1.md, п. 1. Для P1-1 уточнено, что речь о D05, а не об 11 согласованных строках.

3. **Исправлено: D — попытки, не независимые барьеры.** [D/RESULTS.md](../../check-2-law/channels/RESULTS.md), строка 7, прямо запрещает считать 40 отказов независимыми барьерами. [D/REVIEW.md](../../check-2-law/channels/REVIEW.md), пп. 3–4, отмечает лишний отказ passwd и остановку на объявленных запускателях. В REPORT перечислены nohup, tmux, cron, flatpak, bwrap и userns; итог **?** сохранён.

4. **Исправлено: причина сбоя P8-5.** По P/P8-5.md, строки 64 и 75, при истечении аренды в опытах NetworkManager падал тестовый `dns.py`: `sendto ENETUNREACH`, 8/8 основных случаев и 3/3 повторов. REPORT теперь относит сбой к DNS-серверу стенда: стенд **0**, менеджер и гипотеза **?**.

5. **Исправлено: возражение по W.** [W/RESULT.md](../guix/RESULT.md), строки 56–60, решал четыре log-строки через общий объект P6. [W/REVIEW.md](../guix/REVIEW.md), п. 5, это отвергает: shepherd создаёт файл, daemon нуждается в нём; P6 не устанавливает недостающего владельца по §5.1. В REPORT строки названы нерешёнными; итог W **0** сохранён.

6. **Не исправлено: числа REPORT совпадают с результатами.** Сверены A, [V](../debian-fedora-coreos-nixos/RESULT.md), [E6C](../samples/ubuntu-alpine/E6C-RESULT.md), [W](../guix/RESULT.md), [X1C](../samples/arch-silverblue-freebsd/X1C-RESULT.md), [X2C](../samples/debian-desktop/X2C-RESULT.md), X8, P5-7, [P7-3](../../check-4-lifecycle/stands/P7-3.md), P9-3, P3-5 и P8-5. Все 23 пары карточек программно сопоставлены с K/whatif-summary.tsv: совпали; 16 273 наблюдения и срез 13:41:14 UTC подтверждены K/CARDS.md. Оговорка к самому замечанию: P/P6-5.md, строка 80, говорит, что κ не измеряли. REPORT её и не приводит.

7. **Не исправлено: пять свидетельств подтверждают текст REPORT.** В записи переписи личных машин (не публикуется) есть личная настройка с исполняемым кодом; оговорка REPORT об отсутствии трассы исполнения сохранена. [D/continuation-revoke.json](../../check-2-law/channels/raw/d2-stand/results-extra/continuation-revoke.json) подтверждает PID 8108, starttime 43263, heartbeat 3→7 и отказ нового запуска с rc 126. [BQ/summary.json](../../check-3-reproducibility/stand-pair/raw/q/repro/summary.json) подтверждает 1101/31/43/138/52/8, userspace 20/20, всего 88/89 и kernel tasks 68/69. [E3/events.jsonl](../../check-4-lifecycle/rollback/raw-E3/events.jsonl), строки 25–26 и 41–45, подтверждает отказ Firefox 115 от нового профиля и рабочий старый снимок без `after=v128`. P1-2/summary.json и requests.tsv подтверждают 0/16→16/16, 4 чтения и окно 1,284628658 с; PRIME и NC — отдельные контроли.

Ссылка в конце REPORT теперь различает прежнюю рецензию AGREED и последующую DISAGREE и ведёт к этому списку исправлений. Общая сводка пяти проверок не меняется: **0 / ? / ? / ? / ?**.

Независимая проверка: AGREED. Копия отчёта до правок сохранена в tmp/frep/REPORT-before.md.
