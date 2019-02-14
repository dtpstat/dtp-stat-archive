<template>
  <div class="container text">
    <p>
      Проект "Карта ДТП" посвящен проблеме дорожно-транспортных происшествий в России. К сожалению, качество
      дорожной инфраструктуры и городской среды приводит к большому количеству жертв – в 2017 году на дорогах
      страны погибло 19088 человек.
    </p>
    <p>
      Цель проекта - повышение безопасности дорожного движения и снижение смертности в ДТП. "Карта ДТП" не только
      собирает данные о ДТП, но и помогает экспертам, активистам, журналистам и прочим неравнодушным анализировать
      их. Всё это может способствовать выявлению реальных причин ДТП, оценке инфраструктуры, а также выработке
      более качественных программ по повышению безопасности на дорогах.
    </p>
    <P>
      Мы используем данные с официального портала
      <a href="http://stat.gibdd.ru" target="_blank">
        статистики
        ГИБДД
      </a>. Из-за ошибок в исходных данных наш сервис также может содержать неточности.
    </P>
    <br>
    <h4>Добавление собственных маркеров на карту</h4>
    <p>Вы можете добавлять собственные маркеры на карту, чтобы проводить исследования по сторонним объектам - школам, переходам и т.д. Для этого на панели фильтров внизу ест ькнопка, куда необходимо загрузить файл в формет json.</p>
    <p>Формат:</p>
    <figure class="highlight">
      <pre><code>
[
  {
    "name": "Школа",
    "longitude": 37.625385,
    "latitude": 55.751352
  },
  ...
]
        </code></pre>
    </figure>
    <br>
    <br>
    <h4>Контакты</h4>
    <div class="row">
      <div class="col-6">
        <img src="../assets/ustnv.jpg" %}"
        style="max-width: 80%;margin: 20px" class="rounded-circle">
        <b>Сергей Устинов</b>
        <p style="margin: 0">Отвечает за технические вопросы</p>
        <a href="https://www.facebook.com/ustnv.s">https://www.facebook.com/ustnv.s</a>
      </div>
      <div class="col-6">
        <img src="../assets/rad.jpg" %}"
        style="max-width: 80%;margin: 20px" class="rounded-circle">
        <b>Алексей Радченко</b>
        <p style="margin: 0">Отвечает за развитие</p>
        <a href="https://www.facebook.com/alexradchenko">https://www.facebook.com/alexradchenko</a>
      </div>
    </div>
    <br>
    <br>
    <h4 id="media">СМИ о нас</h4>
    <ul>
      <li>
        <a href="https://daily.afisha.ru/news/18145-aktivisty-sozdali-kartu-vseh-dtp-v-moskve/">
          <b>Афиша</b> - Активисты создали карту всех ДТП в Москве
        </a>
      </li>
      <li>
        <a href="https://www.the-village.ru/village/city/news-city/317621-karta-dtp">
          <b>The Village</b> - Интерактивная статистика ДТП на улицах Москвы
        </a>
      </li>
      <li>
        <a href="https://360tv.ru/news/obschestvo/sozdana-onlajnkarta-dtp-moskvy/">
          <b>Телеканал 360</b> - оздана онлайн‐карта ДТП Москвы
        </a>
      </li>
      <li>
        <a
          href="https://tjournal.ru/73169-moskovskie-aktivisty-zapustili-onlayn-kartu-vseh-dtp-v-gorode"
        >
          <b>Tjournal</b> - Московские активисты запустили онлайн-карту всех ДТП в городе
        </a>
      </li>
      <li>
        <a href="https://www.msk.kp.ru/daily/26851/3893361/">
          <b>Комсомольская правда</b> - В Москве опубликовали карту ДТП за последние три года
        </a>
      </li>
      <li>
        <a href="https://rg.ru/2018/07/04/reg-cfo/v-moskve-razrabotali-narodnuiu-kartu-dtp.html">
          <b>Российская газета</b> - В Москве разработали народную карту ДТП
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "dpt-about"
};
</script>
