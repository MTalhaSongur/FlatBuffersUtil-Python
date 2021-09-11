from vd_wrapper import vd_list, vd_wrapper, dict_list


class FlatBuffersUtils:

    @staticmethod
    def serializeDict(params, builder):
        appendedKeys = []
        appendedValues = []
        keyValuePairs = []

        for key in params.keys():
            appendedKeys.append(builder.CreateString(key))

        for valueList in params.values():
            appendedValues.append([])
            for value in valueList:
                appendedValues[-1].append(builder.CreateString(value))

        index = 0
        for valueList in appendedValues:
            dict_list.dict_listStartValuesVector(builder, len(appendedValues[index]))
            for value in valueList:
                builder.PrependSOffsetTRelative(value)
            valueList_to_add = builder.EndVector()
            dict_list.Start(builder)
            dict_list.AddKeys(builder, appendedKeys[index])
            dict_list.AddValues(builder, valueList_to_add)
            builded = dict_list.End(builder)
            keyValuePairs.append(builded)
            index += 1

        vd_list.StartVdListDictVector(builder, len(keyValuePairs))
        for pair in keyValuePairs:
            builder.PrependSOffsetTRelative(pair)
        vd_to_add = builder.EndVector()
        vd_list.Start(builder)
        vd_list.AddVdListDict(builder, vd_to_add)
        finishedVector = vd_list.End(builder)
        builder.Finish(finishedVector)
        buf = builder.Output()
        return buf

    @staticmethod
    def serializeList(params, builder):
        appendedObj = []
        for param in params:
            appendedObj.append(builder.CreateString(param))
        for i in range(len(appendedObj)):
            builder.PrependSOffsetTRelative(appendedObj[i])
        vd_list.StartDataListVector(builder, len(params))
        confList = builder.EndVector()
        vd_list.Start(builder)
        vd_list.AddDataList(builder, confList)
        builded = vd_list.End(builder)
        builder.Finish(builded)
        buf = builder.Output()
        return buf
