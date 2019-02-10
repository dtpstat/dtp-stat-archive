<template>
  <div>
    <dpt-search></dpt-search>
    <dtp-summary></dtp-summary>
    <dtp-partners></dtp-partners>
  </div>
</template>

<script>
import DTPSearch from "@/components/DTPSearch";
import DTPSummary from "@/components/DTPSummary";
import DTPPartners from "@/components/DTPPartners";
export default {
  name: "dtp-index",
  components: {
    "dpt-search": DTPSearch,
    "dtp-summary": DTPSummary,
    "dtp-partners": DTPPartners
  }
};
</script>
