<template>
  <div class="panel-with-overlay">
    <div class="main-content-area" ref="{this.setMainContentAreaRef}">{this.props.children}</div>

    <div class="overlay-area" ref="{this.setOverlayRef}">{this.props.overlay}</div>
  </div>
</template>

<script>
export default {
    name: "dtp-panel-overlay"
}
</script>
