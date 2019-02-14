<template>
  <div class="value_preposition">
    <div class="container">
      <form class="find-region">
        <div class="form-group">
          <input
            type="text"
            id="regionSearch"
            class="form-control"
            placeholder="Введите название района/города/региона"
          >
        </div>
      </form>
      <div class="region-list">
        <p class="item">
          <router-link :to="{ name: 'Area' }">Все города</router-link>
        </p>
        <p class="item">
          <a href="/area?parent_region_name=москва">Москва</a>
        </p>
        <p>
          <a href="/sankt-peterburg/">Санкт-Петербург</a>
        </p>
        <p>
          <a href="/respublika-tatarstan-tatarstan_kazan/">Казань</a>
        </p>
        <p>
          <a href="/nizhegorodskaia-oblast_nizhnii-novgorod/">Нижний Новгород</a>
        </p>
        <p class="item">
          <a href="/krasnodarskii-krai_krasnodar/">Краснодар</a>
        </p>
        <p class="item">
          <a href="/iaroslavskaia-oblast_iaroslavl/">Ярославль</a>
        </p>
        <p class="item">
          <a href="/kirovskaia-oblast_kirov/">Киров</a>
        </p>
        <p class="item">
          <a href="/vladimirskaia-oblast_vladimir/">Владимир</a>
        </p>
        <p class="item">
          <a href="/chuvashskaia-respublika-chuvashiia_cheboksary/">Чебоксары</a>
        </p>
      </div>
    </div>
  </div>
</template>