from goods_owner.serializers import Base_ModelSerializer
from accounts.models import CarrierOwner
from carrier_owner.models import RoadFleet, RequiredCarrier, CarOwReqGoodsOwner
from goods_owner.models import InnerCargo, InternationalCargo, GoodsOwnerReqCarOw


# اطلاعات قابل نمایش صاحب حمل کننده برای صاحب بار
class InfoCarrierOwnerResForGoodsOwnerSerializers(Base_ModelSerializer):
    class Meta:
        model = CarrierOwner
        fields = (
            'id',
            'owner_full_name',
        )


# اطلاعات قابل نمایش حمل کننده برای صاحب بار
class InfoRoadFleetForGoodsOwnerSerializers(Base_ModelSerializer):
    class Meta:
        model = RoadFleet
        fields = Base_ModelSerializer.Meta.fields + (
            'ownerType',
            'roomType',
            'vehichleType',
            'semiHeavyVehichle',
            'semiHeavyVehichleOthers',
            'HeavyVehichle',
            'heavy_vehicle_others',
            'plaque_one_num_check',
            'plaque_puller_num_check',
            'plaque_carriage_num_check',
            'plaque_container_num_check',
            'vehicle_card_bool',
            'vehicle_property_doc_bool',
            'vehicle_advocate_bool',
            'international_docs_bool',
        )


# اطلاعات قابل نمایش بار داخلی برای صاحب بار
class InfoInnerCargoForGoodsOwnerSerializers(Base_ModelSerializer):
    class Meta:
        model = InnerCargo
        fields = Base_ModelSerializer.Meta.fields + (
            'length',
            'width',
            'height',
            'cargoType',
            'pkgType',
            'description',
            'specialWidgets',
            'storageBillNum',
            'storagePrice',
            'loadigPrice',
            'basculPrice',
            'specialDesc',
            'sendersName',
            'sendersFamName',
            'senderMobileNum',
            'dischargeTimeDate',
            'duratio_ndischargeTime',
            'country',
            'delivery_provider_name',
            'delivery_provider_national_id',
            'delivery_provider_full_name',
            'delivery_provider_mobile',
            'cargo_receiver_name',
            'cargo_receiver_national_id',
            'cargo_receiver_full_name',
            'cargo_receiver_mobile',
            'state',
            'city',
            'street',
            'address',
            'customName',
            'deliveryTimeDate',
        )


# اطلاعات قابل نمایش بار خارجی برای صاحب بار

class InfoInternationalCargoForGoodsOwnerSerializers(Base_ModelSerializer):
    class Meta:
        model = InternationalCargo
        fields = Base_ModelSerializer.Meta.fields + (
            'length',
            'width',
            'height',
            'cargoType',
            'pkgType',
            'description',
            'specialWidgets',
            'storageBillNum',
            'storagePrice',
            'loadigPrice',
            'basculPrice',
            'specialDesc',
            'sendersName',
            'sendersFamName',
            'senderMobileNum',
            'dischargeTimeDate',
            'duratio_ndischargeTime',
            'country',
            'delivery_provider_name',
            'delivery_provider_national_id',
            'delivery_provider_full_name',
            'delivery_provider_mobile',
            'cargo_receiver_name',
            'cargo_receiver_national_id',
            'cargo_receiver_full_name',
            'cargo_receiver_mobile',
            'state',
            'city',
            'street',
            'address',
            'customName',
            'senderCountry',
            'senderState',
            'senderCity',
            'senderStreet',
            'senderAddress',
            'deliveryTimeDate',
            'dischargeTimeDate',
            'dischargeTime',
            'customNameEnd',
        )


# اطلاعات قابل نمایش حمل کننده های مورد نیاز برای صاحب بار
class InfoRequiredCarrierForGoodsOwnerSerializers(Base_ModelSerializer):
    inner_cargo_full = InfoInnerCargoForGoodsOwnerSerializers(source='inner_cargo', read_only=True)
    international_cargo_full = InfoInternationalCargoForGoodsOwnerSerializers(source='international_cargo',
                                                                              read_only=True)

    class Meta:
        model = RequiredCarrier
        fields = Base_ModelSerializer.Meta.fields + (
            'relinquished',
            'cargo_type',
            'inner_cargo',
            'inner_cargo_full',
            'international_cargo',
            'international_cargo_full',
            'cargo_weight',
            'counter',
            'room_type',
            'vehichle_type',
            'semi_heavy_vehichle',
            'semi_heavy_vehichle_others',
            'heavy_vehichle',
            'heavy_vehichle_others',
            'special_widget_carrier',
            'carrier_price',
            'cargo_price',
        )


########################################################################################
# اطلاعات قابل نمایش درخواست  همکاری صاحب حمل کننده برای برای صاحب بار

class InfoCarOwReqGoodsOwnerForGoodsOwnerSerializers(Base_ModelSerializer):
    carrier_owner_full = InfoCarrierOwnerResForGoodsOwnerSerializers(source='cargo_owner', read_only=True)
    road_fleet_full = InfoRoadFleetForGoodsOwnerSerializers(source='road_fleet', read_only=True)
    required_carrier_full = InfoRequiredCarrierForGoodsOwnerSerializers(source='required_carrier', read_only=True)

    class Meta:
        model = CarOwReqGoodsOwner
        fields = Base_ModelSerializer.Meta.fields + (
            'user',
            'carrier_owner',
            'carrier_owner_full',
            'road_fleet',
            'road_fleet_full',
            'goods_owner',
            'required_carrier',
            'required_carrier_full',
            'proposed_price',
            'request_result',
            'cancellation_time',
        )


# پایان بخش نمایش درخواست های همکاری دریافتی
################################################################################################
class InfoGoodsOwnerReqCarOwForGoodsOwnerSerializers(Base_ModelSerializer):
    carrier_owner_full = InfoCarrierOwnerResForGoodsOwnerSerializers(source='carrier_owner', read_only=True)
    road_fleet_full = InfoRoadFleetForGoodsOwnerSerializers(source='road_fleet', read_only=True)
    inner_cargo_full = InfoInnerCargoForGoodsOwnerSerializers(source='inner_cargo', read_only=True)
    international_cargo_full = InfoInternationalCargoForGoodsOwnerSerializers(source='international_cargo',
                                                                              read_only=True)

    class Meta:
        model = GoodsOwnerReqCarOw
        fields = Base_ModelSerializer.Meta.fields + (
            'user',
            'goods_owner',
            'carrier_owner',
            'carrier_owner_full',
            'road_fleet',
            'road_fleet_full',
            'inner_cargo',
            'inner_cargo_full',
            'international_cargo',
            'international_cargo_full',
            'proposed_price',
            'request_result',
            'cancellation_time',
        )
