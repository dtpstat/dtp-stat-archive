<template>
  <div class="CheckBox" id="checkbox-div-7">
    <input type="checkbox" v-model="state">
    <span :class="circleClass"></span>
    - {{label}}
  </div>
</template>


<script>
export default {
  name: "dtp-mvctype-checkbox",
  props: {
    type: String,
    label: String,
    handleChangeState: Function
  },
  data() {
    return {
      state: true
    };
  },
  computed: {
    circleClass() {
      switch (this.type) {
        case "auto":
          return "legend-circle color-auto";
        case "bicycle":
          return "legend-circle color-bicycle";
        case "pedestrian":
          return "legend-circle color-pedestrian";
        default:
          return "legend-circle color-auto";
      }
    }
  },
  watch: {
    state(val) {
      this.handleChangeState(val);
    }
  }
};
</script>
