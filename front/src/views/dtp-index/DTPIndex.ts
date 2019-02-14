import { Component, Prop, Vue } from 'vue-property-decorator';
import DTPSearch from "@/components/dtp-search/DTPSearch";
import DTPSummaryStat from "@/components/dtp-summary-stat/DTPSummaryStat";
import DTPPartners from "@/components/dtp-partners/DTPPartners";

@Component({
    components: {
        "dtp-search": DTPSearch,
        "dtp-summary-stat": DTPSummaryStat,
        "dtp-partners": DTPPartners
    }
})
export default class DTPIndex extends Vue { }
