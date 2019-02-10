<template>
  <nav class="navbar topbar navbar-expand">
    <div class="container">
      <router-link class="navbar-brand" :to="{ name: 'Index' }">
        <img src="../assets/logo.png" style="width: 50px;height: auto;margin-right: 10px"> Карта ДТП
      </router-link>

      <ul class="nav navbar-nav ml-auto">
        <h3>
          <a href="https://twitter.com/dtp_stat">
            <i class="fa fa-twitter-square" aria-hidden="true"></i> dtp_stat
          </a>
        </h3>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  name: "dtp-navbar"
};
</script>
