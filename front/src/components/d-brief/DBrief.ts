import { Component, Prop, Vue } from 'vue-property-decorator';

export default class DBrief extends Vue {
    @Prop() private dead!: Number;
    @Prop() private deadAuto!: Number;
    @Prop() private deadBicycle!: Number;
    @Prop() private deadPedestrian!: Number;
    @Prop() private injured!: Number;
    @Prop() private injuredAuto!: Number;
    @Prop() private injuredBicycle!: Number;
    @Prop() private injuredPedestrian!: Number;
    @Prop() private mvcCount!: Number;
}