import { Component, Prop, Vue } from 'vue-property-decorator';
import DSearch from "@/components/d-search/DSearch";
import DPartners from "@/components/d-partners/DPartners";
import DSummary from "@/components/d-summary/DSummary";

@Component({
    components: {
        "d-summary": DSummary,
        "dtp-search": DSearch,
        "dtp-partners": DPartners
    }
})
export default class DIndex extends Vue { }
