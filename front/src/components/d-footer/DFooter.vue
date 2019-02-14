<template>
  <footer>
    <div class="container">
      <div class="row">
        <div class="col-md-6 license text-left" style>
          <div style="max-width: 500px;margin: 0 auto;">
            <div style="float: left;margin: 10px 30px 10px 10px">
              <a href="http://creativecommons.org/licenses/by/4.0/" target="_blank">
                <img src="@/assets/creative-commons-1.png">
                <img src="@/assets/creative-commons-2.png">
              </a>
            </div>

            <p>
              Использование материалов возможно с указанием активной ссылки на сайт. Источник данных -
              <a
                href="http://stat.gibdd.ru"
                target="_blank"
              >ГИБДД</a>.
            </p>
          </div>
        </div>
        <div class="col-md-6 text-center footer-menu" style>
          <router-link :to="{ name: 'Index' }">Главная</router-link>
          <router-link :to="{ name: 'About' }">О проекте</router-link>
          <a href="mailto:info@dtp-stat.ru">info@dtp-stat.ru</a>
        </div>
      </div>
    </div>
  </footer>
</template>